import os
import cv2
import base64
import numpy as np
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from src.detector import analyze_frame

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('process_frame')
def handle_frame(data):
    try:
        # data is a base64 encoded string
        img_data = data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return

        frame, score, state, issues = analyze_frame(frame)

        # Encode processed frame to base64
        _, buffer = cv2.imencode('.jpg', frame)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        emit('frame_processed', {
            'image': 'data:image/jpeg;base64,' + encoded_image,
            'score': score,
            'state': state,
            'issues': issues
        })
    except Exception as e:
        print(f"Error processing frame: {e}")

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)