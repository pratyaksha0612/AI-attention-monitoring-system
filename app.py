from flask import Flask, render_template, Response, jsonify
import cv2
from src.detector import analyze_frame

app = Flask(__name__)

camera = cv2.VideoCapture(0)

latest_data = {
    "state": "Detecting",
    "score": 0,
    "issues": []
}

def generate_frames():
    global latest_data

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        frame, score, state, issues = analyze_frame(frame)

        latest_data = {
            "state": state,
            "score": score,
            "issues": issues
        }

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/data')
def data():
    return jsonify(latest_data)


if __name__ == "__main__":
    app.run(debug=True)