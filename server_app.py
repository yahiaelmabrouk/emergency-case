import cv2
import mediapipe as mp
from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np
import math
import time

app = Flask(__name__)
socketio = SocketIO(app)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# List to store fallen messages
fallen_messages = []

def draw_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, color=(255, 255, 255), thickness=1):
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

# Function to draw a filled rectangle
def draw_filled_rectangle(image, start_point, end_point, color):
    cv2.rectangle(image, start_point, end_point, color, cv2.FILLED)

# Function to detect falls
def detect_fall(landmarks, image_height):
    # Convert normalized y-coordinates to absolute pixel values
    left_shoulder_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_height)
    left_hip_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height)
    right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height)
    right_hip_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image_height)
    fall_threshold = 40 
    # Check if the difference between shoulder and hip y-coordinates is less than the threshold
    if left_hip_y - left_shoulder_y < fall_threshold or right_hip_y - right_shoulder_y < fall_threshold:
        return True
    else:
        return False

# Function to calculate angle between 3 points
def calculate_angle(a, b, c):
    a = np.array(a)  # first 
    b = np.array(b)  # mid
    c = np.array(c)  # last
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 108.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def normalize_distance(distance, reference_distance):
    return distance / reference_distance

# Function for distress detection
def distress_detection(landmarks, image, duration=10):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

    # Calculate the distance between the shoulders
    shoulder_distance = calculate_distance(left_shoulder, right_shoulder)

    # Normalize distances by dividing by shoulder distance
    distance_left_hand_shoulder_normalized = normalize_distance(
        calculate_distance(left_hand, left_shoulder),
        shoulder_distance
    )
    distance_right_hand_shoulder_normalized = normalize_distance(
        calculate_distance(right_hand, right_shoulder),
        shoulder_distance
    )

    # Calculate the angle between left elbow, left wrist, and left shoulder
    angle_left_arm = calculate_angle(
        [left_elbow.x, left_elbow.y],
        [left_hand.x, left_hand.y],
        [left_shoulder.x, left_shoulder.y]
    )

    # Calculate the angle between right elbow, right wrist, and right shoulder
    angle_right_arm = calculate_angle(
        [right_elbow.x, right_elbow.y],
        [right_hand.x, right_hand.y],
        [right_shoulder.x, right_shoulder.y]
    )
    distress_flag = False
    # Check if it's time to print
    current_time = time.time()
    if (
        (0.5 < distance_right_hand_shoulder_normalized < 1 and (110 < angle_right_arm < 145 or 60 < angle_left_arm < 100)) or
        (0.2 < distance_left_hand_shoulder_normalized < 0.8 and (110 < angle_right_arm < 145 or 60 < angle_left_arm < 100))
    ):
        distress_detection.last_print_time = current_time

        # Display "warning" text during the countdown
        draw_text(image, "warning", (20, 100), color=(0, 0, 255))

        if not hasattr(distress_detection, 'start_time'):
            distress_detection.start_time = current_time
        elif current_time - distress_detection.start_time > duration:
            countdown = int(duration - (current_time - distress_detection.start_time))

            # Display the countdown
            draw_text(image, str(countdown), (20, 70), color=(255, 0, 0))

            if countdown <= 10:
                # Switch to "danger" text
                draw_text(image, "danger", (20, 100), color=(255, 0, 0))

            if countdown <= 0:
                distress_flag = True
    else:
        # Reset the variables when the condition is not satisfied
        distress_detection.start_time = None
        distress_detection.last_print_time = None

    return distress_flag

# Function to clear fallen messages
def clear_fallen_messages():
    fallen_messages.clear()

# Video capture and pose detection loop
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened(): 
        ret, frame = cap.read()
        # Recolor image 
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Make detection 
        results = pose.process(image)
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Extract landmarks 
        try:
            landmarks = results.pose_landmarks.landmark
            if distress_detection(landmarks, image):
                socketio.emit('heart_distress_alert', {'message': 'Heart distress detected!'})
            # Draw text on the image to display fall state
            if detect_fall(landmarks, image.shape[0]):
                socketio.emit('fall_alert', {'message': 'Fall detected!'})
                text = "Fallen"
            
            draw_text(image, text, (20, 40), color=(255, 255, 255), font_scale=2.0)

        except Exception as e:
            pass 
            
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Mediapipe Feed', image)
        
        if cv2.waitKey(10) & 0xFF == ord("q"): 
            break

cap.release()
cv2.destroyAllWindows()

# Route to clear fallen messages
@app.route('/clear_fallen_messages')
def clear_messages_route():
    clear_fallen_messages()
    return 'Fallen messages cleared!'

# Route to display fallen messages
@app.route('/fallen_messages')
def fallen_messages():
    return render_template('messages.html')

@app.route('/')
def index():
    return render_template('server/index.html')

@socketio.on('fall_detection_result')
def handle_fall_detection_result(data):
    landmarks = data['landmarks']
    image_height = data['image_height']
    
    fall_detected = detect_fall(landmarks, image_height)
    heart_distress = distress_detection(landmarks, image)
    fallen_messages.append({'fall_detected': fall_detected, 'heart_distress': heart_distress})
    
    # Print messages for debugging
    print(f"Fall detected: {fall_detected}, Heart distress: {heart_distress}")

    # Send a message indicating fall detection or heart distress
    if fall_detected:
        socketio.emit('fall_alert', {'message': 'Fall detected!'})
    elif heart_distress:
        socketio.emit('heart_distress_alert', {'message': 'Heart distress detected!'})

@socketio.on('fetch_fallen_messages')
def handle_fetch_fallen_messages():
    socketio.emit('update_fallen_messages', {'fallen_messages': fallen_messages})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the Flask app with SocketIO
    socketio.run(app, debug=True)
