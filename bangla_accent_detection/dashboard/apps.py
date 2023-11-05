from django.apps import AppConfig

# model loading libraries
import tensorflow as tf
import pickle


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'


# class for loading the trained model
class MyAppConfig(AppConfig):
    model = tf.keras.models.load_model('models/ANN_Model_val_acc_90%.h5')
