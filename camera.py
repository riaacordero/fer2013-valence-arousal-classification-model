import cv2
from model import FacialExpressionModel
import numpy as np
import pickle
from emotion_mapping import emotion_to_valence_arousal

facec = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

# Load the mapping
with open('emotion_to_vac.pkl', 'rb') as f:
    emotion_to_valence_arousal = pickle.load(f)
    
class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(0)  # 0 means the default webcam
        self.video = cv2.VideoCapture('test_video/bbc_news.mp4')  # replace 'your_video_file.mp4' with your file name

    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            roi_rgb = np.repeat(roi[..., np.newaxis], 3, -1)
            preds = model.predict_emotion(roi_rgb[np.newaxis, ...])[0]

            # Print out the predictions
            print("Predictions:", preds)

            # Get the emotion with the highest probability
            emotion = FacialExpressionModel.EMOTIONS_LIST[np.argmax(preds)]
            # emotion = emotion.title()  # remove or comment out this line
            valence, arousal = emotion_to_valence_arousal[emotion]

            # Display the emotion, valence, and arousal on the frame
            cv2.putText(fr, f'Valence: {valence:.2f}', (x, y + h + 20), font, 1, (255, 255, 0), 2)
            cv2.putText(fr, f'Arousal: {arousal:.2f}', (x + w + 10, y + h // 2), font, 1, (255, 255, 0), 2)

            # Draw bounding box
            cv2.rectangle(fr, (x, y), (x + w, y + h), (255, 0, 0), 2)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()