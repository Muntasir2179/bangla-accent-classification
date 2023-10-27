from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def make_prediction(request):
    return render(request, 'main.html')