//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var cancelButton = document.getElementById("cancelButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
cancelButton.addEventListener("click", cancelRecording);

function startRecording() {
  console.log("recordButton clicked");

  /*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

  var constraints = { audio: true, video: false };

  /*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

  recordButton.disabled = true;
  stopButton.disabled = false;
  cancelButton.disabled = false;

  // Removing previous recording and file
  document.getElementById("recordingsList").innerHTML = "";
  document.getElementById("recordingFile").value = "";
  document.getElementById("predictionOperation").style.display = "none";

  /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      console.log(
        "getUserMedia() success, stream created, initializing Recorder.js ..."
      );

      audioContext = new AudioContext();

      /*  assign to gumStream for later use  */
      gumStream = stream;

      /* use the stream */
      input = audioContext.createMediaStreamSource(stream);

      rec = new Recorder(input, { numChannels: 2 });

      //start the recording process
      rec.record();

      // Recording Sections show/hide operation
      document.getElementById("startRecordingSection").style.display = "none";
      document.getElementById("runningRecordingSection").style.display =
        "block";

      // Timer Functions
      startTimer();

      console.log("Recording started");
    })
    .catch(function (err) {
      // Recording Sections show/hide operation
      document.getElementById("startRecordingSection").style.display = "block";
      document.getElementById("runningRecordingSection").style.display = "none";

      // Timer Functions
      clearInterval(timerInterval);
      resetTimer();

      //enable the record button if getUserMedia() fails
      recordButton.disabled = false;
      stopButton.disabled = true;
      cancelButton.disabled = true;
    });
}

function cancelRecording() {
  console.log("cancelButton clicked");

  //disable the stop button, enable the record too allow for new recordings
  recordButton.disabled = false;
  stopButton.disabled = true;
  cancelButton.disabled = true;

  //tell the recorder to stop the recording
  rec.stop();

  //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  // Recording Sections show/hide operation
  document.getElementById("startRecordingSection").style.display = "block";
  document.getElementById("runningRecordingSection").style.display = "none";

  // Timer Functions
  clearInterval(timerInterval);
  resetTimer();

  console.log("cancelButton action ends");
}

function stopRecording() {
  console.log("stopButton clicked");

  //disable the stop button, enable the record too allow for new recordings
  stopButton.disabled = true;
  recordButton.disabled = false;
  cancelButton.disabled = true;

  //tell the recorder to stop the recording
  rec.stop();

  //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  // Recording Sections show/hide operation
  document.getElementById("startRecordingSection").style.display = "block";
  document.getElementById("runningRecordingSection").style.display = "none";

  // Timer Functions
  clearInterval(timerInterval);
  resetTimer();

  //create the wav blob and pass it on to createDownloadLink
  rec.exportWAV(createDownloadLink);

  console.log("stopButton actions ends");
}

function createDownloadLink(blob) {
  // Send recorded Blob to server
  const formData = new FormData();
  formData.append("audio", blob, "recording.wav");

  // show/hide processing animation
  document.getElementById("no_recording").style.display = "none";
  document.getElementById("recording_processing").style.display = "block";

  $.ajax({
    url: "http://localhost:3600/audio-processing",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (data) {
      if (data.audio.src) {
        fetch(data.audio.src)
          .then((response) => response.blob())
          .then((blob) => {
            var url = URL.createObjectURL(blob);
            var au = document.createElement("audio");
            var li = document.createElement("li");
            var link = document.createElement("a");

            //name of .wav file to use during upload and download (without extension)
            var filename = new Date().toISOString();

            //add controls to the <audio> element
            au.controls = true;
            au.src = url;

            //save to disk link
            link.href = url;
            link.download = filename + ".wav"; //download forces the browser to download the file using the  filename
            link.innerHTML = "<i class='fa-solid fa-download'></i>";

            //add the new audio element to li
            li.appendChild(au);

            //add the filename to the li
            li.appendChild(document.createTextNode(filename + ".wav "));

            //add the save to disk link to li
            li.appendChild(link);

            //add the li element to the ol
            recordingsList.appendChild(li);

            console.log("Entered into audio file creation");

            // Creating file from blob
            const recordingFile = new File([blob], `${filename}.wav`);

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(recordingFile);

            const recordingInput = document.getElementById("recordingFile");
            recordingInput.files = dataTransfer.files;

            // Showing prediction section
            document.getElementById("predictionOperation").style.display =
              "block";

            // show/hide processing animation
            document.getElementById("recording_processing").style.display =
              "none";
          });
      } else {
        console.log("Error! Try Again. Didn't get the recorded Audio.");
        document.getElementById("recording_processing").style.display = "none";
      }
    },
    error: function (xhr, status, error) {
      console.error("Upload failed:", error);
      document.getElementById("recording_processing").style.display = "none";
    },
  });
}

// Timer Coding
let mins = 0;
let seconds = 0;
let timerInterval;
let timerCount = 0;
let countIterations = 0;

let timeLimitInSeconds = 300; // 1m = 60s, 5m = 300s
// $("#startTimer").click(function () {
//   startTimer();
// });

// $("#stopTimer").click(function () {
//   clearTimeout(timerInterval);
// });

// $("#resetTimer").click(function () {
//   mins = 0;
//   seconds = 0;
//   $("#timerMins").html("00");
//   $("#timerSeconds").html("00");
// });

function resetTimer() {
  mins = 0;
  seconds = 0;
  $("#timerMins").html("00");
  $("#timerSeconds").html("00");
  clearInterval(timerInterval);
}

function startTimer() {
  // setInterval(() => {
  //   seconds++;
  // }, 1000);
  clearInterval(timerInterval);
  timerInterval = setInterval(function () {
    seconds++;
    countIterations++;
    if (seconds > 59) {
      seconds = 0;
      mins++;
      if (mins < 10) {
        $("#timerMins").text("0" + mins);
      } else $("#timerMins").text(mins);
    }
    if (seconds < 10) {
      $("#timerSeconds").text("0" + seconds);
    } else {
      $("#timerSeconds").text(seconds);
    }
    console.log("Start Timer: " + timerCount++);
    if (countIterations >= timeLimitInSeconds) {
      clearInterval(timerInterval);
      stopRecording();
    }
    // startTimer();
  }, 1000);
}

// Sidebar Functions
//Making the side navigation collapsible
let wholePage = document.getElementById("page_wrapper");
let btn = document.getElementById("nav_collapse_btn");

btn.addEventListener("click", collapse);

function collapse() {
  wholePage.classList.toggle("collapsed");
  if (wholePage.classList.contains("collapsed")) {
    btn.innerHTML = "<i class='bx bxs-chevrons-right'></i>";
  } else {
    btn.innerHTML = "<i class='bx bxs-chevrons-left'></i>";
  }
}
