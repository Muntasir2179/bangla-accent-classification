from django.shortcuts import render, redirect
from .models import Document, AccentData
from .apps import MyAppConfig

# dependencies for trained model
import pickle
import numpy as np
import librosa
import time


# functions for handling model and audio features
# loading the model and making prediction
def predict_accent(features):
    model = MyAppConfig.model
    prediction_probabilities = model.predict(
        features.reshape(-1, 128), verbose=0)
    # removing single dimension
    prediction_probabilities = prediction_probabilities.squeeze()
    return prediction_probabilities

# audio feature extractor function


def features_extractor(file_name):
    time_load = time.time()
    audio, sample_rate = librosa.load(
        file_name, res_type='kaiser_fast', mono=False, sr=None)
    print(time.time() - time_load, "Audio loading time")

    time_extraction = time.time()
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=128)
    print(time.time() - time_extraction, "Time for feature extraction")
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    return mfccs_scaled_features


# functions for request handling
# Create your views here.
def index(request):
    return render(request, 'index.html')


def recording_page(request):
    return render(request, 'recording_page.html')


def make_prediction(request):
    if request.method == "POST":
        if not 'recording_file' in request.FILES or not 'upload_file' in request.FILES:
            title_text = "There is no audio input."
            prediction_probabilities = np.zeros(13)

        # getting the audio file
        if 'recording_file' in request.FILES:
            audio = request.FILES['recording_file']
        elif 'upload_file' in request.FILES:
            audio = request.FILES['upload_file']
        # saving an audio file by creating an Document object
        audio_file = Document.objects.create(name=audio.name, file=audio)
        audio_path = audio_file.file.path
        # loading the onehot encoder
        with open('models/onehot_encoder_accent_classification.pkl', 'rb') as f:
            encoder = pickle.load(f)

        try:

            title_text = "Prediction probabilities for each accent"

            start_fe = time.time()
            # extracting features from the enhanced audio file
            features = features_extractor(audio_path).reshape(-1, 128)
            print(time.time() - start_fe, "Time for extraction")

            model_fe = time.time()
            # making prediction on users input voice
            prediction_probabilities = predict_accent(features=features)
            print(time.time() - model_fe, "Time for prediction")

            # converting the result into onehot representation
            one_hot_output = np.zeros(len(prediction_probabilities))
            one_hot_output[np.argmax(prediction_probabilities)] = 1.0

            # getting the predicted class name
            predicted_class = encoder.inverse_transform(
                one_hot_output.reshape(1, -1)).squeeze()
            # getting prediction confidence
            prediction_confidence = prediction_probabilities[np.argmax(
                prediction_probabilities)]
        except Exception as e:
            title_text = "There is no audio input"
            prediction_probabilities = np.zeros(13)
            predicted_class = None
            prediction_confidence = -1

        # getting all classes names from the encoder
        all_class_names = [class_name.replace(
            'x0_', '') for class_name in encoder.get_feature_names_out()]

        # creating dictionary of class and their corresponding probability score
        probability_dict = dict(zip(all_class_names, prediction_probabilities))

        context = {
            'title_text': title_text,
            'file_name': audio_path,
            'labels': [key for key, _ in probability_dict.items()],
            'probability': [value for _, value in probability_dict.items()],
            'probability_dict': probability_dict,
            'predicted_class': predicted_class,
            'prediction_confidence': prediction_confidence,
        }

    return render(request, 'result.html', context=context)


# saving prediction details to the database
def feedback(request):
    # creating a database object
    accent_data = AccentData()

    # fetching data
    accent_data.file_name = request.POST.get('file_name')
    accent_data.predicted_accent = request.POST.get('predicted_class')
    accent_data.user_prediction = request.POST.get('user_prediction')
    accent_data.predicted_accent_confidence = request.POST.get(
        'prediction_confidence')

    # confidence of each accent
    accent_data.barishal_conf = request.POST.get('barishal')
    accent_data.bogura_conf = request.POST.get('bogura')
    accent_data.chottogram_conf = request.POST.get('chottogram')
    accent_data.kurigram_conf = request.POST.get('kurigram')
    accent_data.madaripur_conf = request.POST.get('madaripur')
    accent_data.mymenshing_conf = request.POST.get('maymenshing')
    accent_data.noakhali_conf = request.POST.get('noakhali')
    accent_data.pabna_conf = request.POST.get('pabna')
    accent_data.puran_dhaka_conf = request.POST.get('puran dhaka')
    accent_data.rajshahi_conf = request.POST.get('rajshahi')
    accent_data.shatkhira_conf = request.POST.get('shatkhira')
    accent_data.sylhet_conf = request.POST.get('sylhet')
    accent_data.tahurgaon_conf = request.POST.get('thakurgaon')

    # string = ''
    # for i in model_prediction:
    #     if i.isalpha():
    #         string += i

    accent_data.is_correct_prediction = (request.POST.get(
        'user_prediction') == request.POST.get('predicted_class'))
    accent_data.save()
    return redirect('recording-page')


def prediction_history(request):
    data = AccentData.objects.all()
    context = {
        'data': data
    }
    return render(request, 'history.html', context=context)
