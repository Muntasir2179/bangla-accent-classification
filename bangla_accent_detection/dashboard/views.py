from django.shortcuts import render
from .models import Document

# dependencies for trained model
import librosa

# Create your views here.

def index(request):
    return render(request, 'index.html')

def recording_page(request):
    return render(request, 'main.html')

def make_prediction(request):
    if request.method == "POST":
        audio = request.FILES['recording_file']
        Document.objects.create(name=audio.name, file=audio)   # saving an audio file by creating an Document object
    return render(request, 'result.html')