from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
from panic_attack import classify_panic_attack, update_html_content

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update-content', methods=['POST'])
def update_content():
    timestamp = request.form['timestamp']
    message = request.form['message']
    return update_html_content(timestamp, message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)