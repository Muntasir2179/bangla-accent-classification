from django.shortcuts import render
from .models import Document

# dependencies for trained model
import tensorflow as tf
import pickle
import numpy as np
import librosa

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
        # getting the audio file
        audio = request.FILES['recording_file']
        audio_file = Document.objects.create(name=audio.name, file=audio)   # saving an audio file by creating an Document object
        audio_path = audio_file.file.path

        # extracting features from the enhanced audio file
        features = features_extractor(audio_path).reshape(-1, 128)
        
        # loading the trained model
        model = tf.keras.models.load_model('models/ANN_Model_val_acc_90%.h5')
        result = model.predict(features.reshape(-1, 128), verbose=0)

        # converting the result into onehot representation
        one_hot_output = np.zeros(13)
        one_hot_output[np.argmax(result)] = 1.0

        with open('models/onehot_encoder_accent_classification.pkl', 'rb') as f:
            encoder = pickle.load(f)
        
        print(encoder.inverse_transform(one_hot_output.reshape(1, -1)).squeeze())

    return render(request, 'result.html')