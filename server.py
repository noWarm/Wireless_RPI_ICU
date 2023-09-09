from flask import Flask, Response, jsonify, request
from flask_socketio import SocketIO
import cv2 as cv
import time
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
w = 640
h = 480
cap.set(3, w)
cap.set(4, h)

watch_state = False

@app.route('/watch_state', methods=['POST'])
def handle_watch_state():
    try:
        data = request.get_json()
        new_state = data.get('state')
        
        global watch_state
        watch_state = new_state
        
        return jsonify({'message': 'toggle watch state success!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
def gen_socket_frame():
    ret, frame = cap.read()   
    img_base64 = base64.b64encode(cv.imencode('.jpg', frame)[1]).decode()
    return img_base64

@socketio.on('express connected')
def express_connect(data):
    print('express connected')
    while True:
        # print(watch_state)
        socketio.emit('data_to_express', gen_socket_frame())
        time.sleep(1)

socketio.run(app, host="0.0.0.0", port=8000)
