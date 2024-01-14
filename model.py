from tensorflow import keras as keras
from keras.models import model_from_json

class FacialExpressionModel(object):
    EMOTIONS_LIST = ["angry", "disgust", "fear", "happy", "sad",  "neutral", "surprise"]

    def __init__(self, model_json_file, model_weights_file):
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()

    def predict_emotion(self, img):
        preds = self.loaded_model.predict(img)
        return preds[0]  # returns (valence, arousal)
