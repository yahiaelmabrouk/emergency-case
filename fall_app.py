import cv2
import mediapipe as mp
import numpy as np
import math
from flask import Flask, render_template, Response

app = Flask(__name__)

def draw_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, color=(255, 255, 255), thickness=1):
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

# ... (your other functions)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize start_time outside the loop
distress_detection.start_time = None

cap = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            distress_flag = distress_detection(landmarks, image)

            start_point = (5, 10)
            end_point = (400, 60)
            rectangle_color = (0, 0, 255)  # Blue color
            draw_filled_rectangle(image, start_point, end_point, rectangle_color)

            if distress_flag or detect_fall(landmarks, image.shape[0]):
                text = "Fallen! Alert!"
            else:
                text = "No Fall Detected"

            draw_text(image, text, (20, 40), color=(255, 255, 255), font_scale=1.0)

        except Exception as e:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        app.run(debug=True)

cap.release()
cv2.destroyAllWindows()
