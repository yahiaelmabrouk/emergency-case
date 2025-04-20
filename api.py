from flask import Flask, Response
import cv2
import mediapipe as mp
import numpy as np

# Flask app setup
app = Flask(__name__)

# Mediapipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to detect falls
def detect_fall(landmarks, image_height):
    try:
        left_shoulder_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_height)
        left_hip_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height)
        right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height)
        right_hip_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image_height)
        fall_threshold = 40
        return (
            left_hip_y - left_shoulder_y < fall_threshold or 
            right_hip_y - right_shoulder_y < fall_threshold
        )
    except Exception as e:
        print(f"Error in fall detection: {e}")
        return False

# Function to generate video frames for streaming
def generate_frames(camera_index):
    cap = cv2.VideoCapture(camera_index)  # Use the selected camera index
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open webcam with index {camera_index}. Check your Iriun Webcam setup.")

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame. Check the webcam connection.")
                break

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Process the image and find pose landmarks
            results = pose.process(image)

            # Recolor back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract pose landmarks
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Detect fall
                if detect_fall(landmarks, image.shape[0]):
                    cv2.putText(image, "Fall Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, "No Fall Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Draw pose landmarks on the image
                mp_drawing.draw_landmarks(
                    image, 
                    results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                )

            # Encode the processed frame
            _, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # Stream the frame as an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Flask route to serve the video stream
@app.route('/video_feed')
def video_feed():
    # Change the camera index if needed (default is 0)
    camera_index = 0  # 0 = Default, 1 = Iriun Webcam (test other indices if needed)
    return Response(generate_frames(camera_index), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route (optional for testing)
@app.route('/')
def index():
    return "Video streaming is active. Access '/video_feed' for the stream."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
