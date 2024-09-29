from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recording-page/', views.recording_page, name='recording-page'),
    path('make-prediction/', views.make_prediction, name='make-prediction'),
    path('feedbaack/', views.feedback, name='feedback'),
    path('prediction-history/', views.prediction_history, name='prediction-history')
]
