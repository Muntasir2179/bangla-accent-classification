require("dotenv").config();
require("express-async-errors");

const express = require("express");
const app = express();

const fs = require("fs");
const { StatusCodes } = require("http-status-codes");
const expressFileUpload = require("express-fileupload");
const axios = require("axios");

const cors = require("cors");

const { v2: cloudinary } = require("cloudinary");
cloudinary.config({
  cloud_name: "dxhbkvt39",
  api_key: "689134944423819",
  api_secret: "pW5r0eBYpdblDimQuHA2LXqyIvw",
});

// error handler
const errorHandlerMiddleware = require("./middleware/error-handler");

app.use(cors());
app.use(express.json());
app.use(expressFileUpload({ useTempFiles: true }));

const startEnhanceJob = async (url) => {
  const authPreApi = Buffer.from(
    `q1inPNJEEz-Tl8IucZOHXg==:9kafGgPi3EfAJOu5EhN1EvhTxJY3ORfZm1SubOHTmXE=`
  ).toString("base64");

  const { data: authApiToken } = await axios({
    method: "post",
    url: "https://api.dolby.io/v1/auth/token",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${authPreApi}`,
    },
    data: {
      grant_type: "client_credentials",
      expires_in: 86400,
    },
  });

  const DOLBY_API_TOKEN = authApiToken.access_token;

  // create a dolby URL
  // const dlbUrl =
  //   "dlb://out/" + url.split("/").slice(-1)[0].split(".")[0] + ".wav";

  const dlbUrl = "dlb://out/enhanced-audio.wav";

  // POST request
  const { data } = await axios({
    method: "post",
    url: "https://api.dolby.com/media/enhance",
    headers: {
      Authorization: `Bearer ${DOLBY_API_TOKEN}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    data: {
      input: url,
      output: dlbUrl,
      content: { type: "interview" },
    },
  });

  return { jobId: data.job_id, dlbUrl };
};

const checkEnhanceJob = async (job_id) => {
  const authPreApi = Buffer.from(
    `q1inPNJEEz-Tl8IucZOHXg==:9kafGgPi3EfAJOu5EhN1EvhTxJY3ORfZm1SubOHTmXE=`
  ).toString("base64");

  const { data: authApiToken } = await axios({
    method: "post",
    url: "https://api.dolby.io/v1/auth/token",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${authPreApi}`,
    },
    data: {
      grant_type: "client_credentials",
      expires_in: 86400,
    },
  });

  const DOLBY_API_TOKEN = authApiToken.access_token;

  const { data } = await axios({
    method: "GET",
    url: "https://api.dolby.com/media/enhance",
    headers: {
      Authorization: `Bearer ${DOLBY_API_TOKEN}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    params: { job_id: job_id },
  });

  // Returns a number between 0 and 100
  return data.progress;
};

const waitUntilJobCompletes = async (job_id) => {
  let progress = await checkEnhanceJob(job_id);
  while (progress < 100) {
    await new Promise((r) => setTimeout(r, 2000));
    progress = await checkEnhanceJob(job_id);
    console.log(progress);
  }
  return;
};

const getNewFileUrl = async (dlbUrl) => {
  const authPreApi = Buffer.from(
    `q1inPNJEEz-Tl8IucZOHXg==:9kafGgPi3EfAJOu5EhN1EvhTxJY3ORfZm1SubOHTmXE=`
  ).toString("base64");

  const { data: authApiToken } = await axios({
    method: "post",
    url: "https://api.dolby.io/v1/auth/token",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${authPreApi}`,
    },
    data: {
      grant_type: "client_credentials",
      expires_in: 86400,
    },
  });

  const DOLBY_API_TOKEN = authApiToken.access_token;

  const { data } = await axios({
    method: "GET",
    url: "https://api.dolby.com/media/output",
    headers: {
      Authorization: `Bearer ${DOLBY_API_TOKEN}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    responseType: "stream",
    params: { url: dlbUrl },
  });

  // console.log(data.url);
  // console.log(data.responseUrl);
  // throw new Error("Get New File Url");
  return data.responseUrl;
};

app.get("/", (req, res) => {
  res.send("<h1>File Upload Starter</h1>");
});

app.post("/audio-processing", async (req, res) => {
  console.log(req.files.audio);

  const result = await cloudinary.uploader.upload(
    req.files.audio.tempFilePath,
    {
      use_filename: true,
      folder: "audio-upload",
      resource_type: "auto",
    }
  );

  if (result.secure_url) {
    fs.unlinkSync(req.files.audio.tempFilePath);

    const { jobId, dlbUrl } = await startEnhanceJob(result.secure_url);

    // track progress as it is processing:
    await waitUntilJobCompletes(jobId);

    // get the output URL:
    const enhanceUrl = await getNewFileUrl(dlbUrl);

    return res.status(StatusCodes.OK).json({ audio: { src: enhanceUrl } });
  } else {
    return res
      .status(StatusCodes.BAD_REQUEST)
      .json({ error: "Audio not enhanced" });
  }
});

// middleware
app.use(errorHandlerMiddleware);

const port = process.env.PORT || 3600;

const start = async () => {
  try {
    app.listen(port, () =>
      console.log(`Server is listening at http://localhost:${port}`)
    );
  } catch (error) {
    console.log(error);
  }
};

start();
