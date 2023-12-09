from django.db import models

from django.db import models
from tensorflow.keras.models import load_model
import cv2
import numpy as np

class CNNModel(models.Model):
    model = load_model('cnn/NOTES.hdf5')

    @staticmethod
    def predict_image(image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (244, 244))
        image = np.expand_dims(image, axis=0)

        prediction = CNNModel.model.predict(image)
        return prediction
    
class Meta:
    app_label = 'cnn'
