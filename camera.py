import cv2
from model import FacialExpressionModel
import numpy as np
import pickle

from emotion_mapping import map_emotion
from panic_attack import PanicAttackClassifier

facec = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

# Load the mapping
with open('emotion_to_vac.pkl', 'rb') as f:
    emotion_to_valence_arousal = pickle.load(f)

# detect_face is a generator function that returns a frame and panic result
def detect_face(frame: cv2.typing.MatLike):
    gray_fr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray_fr, 1.3, 5)

    for (x, y, w, h) in faces:
        # Extract the ROI of the face from the grayscale image, resize it to 48x48, and then prepare
        fc = gray_fr[y:y+h, x:x+w]

        # Resize the image to 48x48 for the model
        roi = cv2.resize(fc, (48, 48))

        # Convert the image to RGB
        roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)

        # Normalize the ROI (convert to float and divide by 255.0)
        roi = roi.astype("float") / 255.0

        # Expand the dimensions to match the input shape of the model (1, 48, 48, 3)
        roi = np.expand_dims(roi, axis=0)

        # Return the ROI and the coordinates of the face
        yield (roi, x, y, w, h)

def predict_from_img(classifier: PanicAttackClassifier, img: cv2.typing.MatLike, timestamp: int):
    valence, arousal = model.predict_emotion(img)
    val, arou = valence, arousal
    if type(valence) == np.float64:
        val = valence.item()
    if type(arousal) == np.float64:
        arou = arousal.item()
    emotion = map_emotion(val, arou)
    result = classifier.classify(val, arou, timestamp)
    return (valence, arousal, emotion, result)
