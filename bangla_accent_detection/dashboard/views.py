from django.shortcuts import render
from .models import Document

# dependencies for trained model
import tensorflow as tf
import pickle
import numpy as np
import librosa
import os
import send2trash as st

# audio feature extractor function
def features_extractor(file_name):
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=128)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features

# Create your views here.

def index(request):
    return render(request, 'index.html')

def recording_page(request):
    return render(request, 'main.html')

def make_prediction(request):
    if request.method == "POST":
        if not 'recording_file' in request.FILES:
            title_text = "There is no audio input."
            prediction_probabilities = np.zeros(13)

        # getting the audio file
        audio = request.FILES['recording_file']
        audio_file = Document.objects.create(name=audio.name, file=audio)   # saving an audio file by creating an Document object
        audio_path = audio_file.file.path

        # loading the onehot encoder
        with open('models/onehot_encoder_accent_classification.pkl', 'rb') as f:
                encoder = pickle.load(f)

        try:
            title_text = "Prediction probabilities for each accent"

            # extracting features from the enhanced audio file
            features = features_extractor(audio_path).reshape(-1, 128)

            # loading the trained model and making prediction on users input voice
            model = tf.keras.models.load_model('models/ANN_Model_val_acc_90%.h5')
            prediction_probabilities = model.predict(features.reshape(-1, 128), verbose=0)
            prediction_probabilities = prediction_probabilities.squeeze()  # removing single dimension

            # converting the result into onehot representation
            one_hot_output = np.zeros(len(prediction_probabilities))
            one_hot_output[np.argmax(prediction_probabilities)] = 1.0
            
            # getting the predicted class name
            predicted_class = encoder.inverse_transform(one_hot_output.reshape(1, -1)).squeeze()
            # getting prediction confidence
            prediction_confidence = prediction_probabilities[np.argmax(prediction_probabilities)]
        except Exception as e:
            title_text = "There is no audio input"
            prediction_probabilities = np.zeros(13)
            predicted_class = None
            prediction_confidence = -1

        # getting all classes names from the encoder
        all_class_names = [class_name.replace('x0_', '') for class_name in  encoder.get_feature_names_out()]

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