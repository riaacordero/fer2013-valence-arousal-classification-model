from keras.models import model_from_json

import numpy as np
import tensorflow as tf
from tensorflow import keras as keras

import matplotlib.pyplot as plt

class FacialExpressionModel(object):
    EMOTIONS_LIST = ["angry", "disgust", "fear", "happy", "sad",  "neutral", "surprise"]

    def __init__(self, model_json_file, model_weights_file):
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]

    def plot_emotions(self, img):
        preds = self.predict_emotion(img)
        fig, ax = plt.subplots()
        ax.scatter(range(len(self.EMOTIONS_LIST)), preds)
        ax.set_xticks(range(len(self.EMOTIONS_LIST)))
        ax.set_xticklabels(self.EMOTIONS_LIST)
        plt.show()