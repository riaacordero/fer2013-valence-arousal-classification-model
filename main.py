from flask import Flask, render_template, Response, jsonify, request
from camera import analyze_frame
from panic_attack import classify_panic_attack, update_html_content
import cv2

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

def gen(video: cv2.VideoCapture):
    """Video streaming generator function."""
    for frame, valence, arousal in analyze_frame(video):
        # Classify panic attack based on valence and arousal
        panic_result = classify_panic_attack(valence, arousal)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
    # Once the video ends, release the video capture
    video.release()

@app.route('/video_feed')
def video_feed():
    video = cv2.VideoCapture('test_files/test_video/bbc_news.mp4')  # 0 means the default webcam
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update-content', methods=['POST'])
def update_content():
    timestamp = request.form['timestamp']
    message = request.form['message']
    return update_html_content(timestamp, message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
