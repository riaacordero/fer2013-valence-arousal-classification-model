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
        self.video = cv2.VideoCapture('test_files/test_video/horrorweb.mp4')  # 0 means the default webcam

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            print("Could not read frame from video source")
            return None

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

            # Predict valence and arousal
            valence, arousal = model.predict_emotion(roi)

            # Display the emotion, valence, and arousal on the frame
            cv2.putText(frame, f'Valence: {valence:.2f}', (x, y + h + 40), font, 1, (255, 255, 0), 2)
            cv2.putText(frame, f'Arousal: {arousal:.2f}', (x, y + h + 160 // 2), font, 1, (255, 255, 0), 2)

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()