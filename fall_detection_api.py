from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import cv2
import numpy as np
import mediapipe as mp
from transformers import pipeline
import pyttsx3
from playsound import playsound
import time
import math

app = FastAPI()

# Mediapipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Text-to-Speech setup
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)
tts_engine.setProperty("volume", 1.0)

# Hugging Face model setup
text_generator = pipeline("text-generation", model="gpt2")

# Alert sound path
ALERT_SOUND_PATH = "alert.wav"

# Helper functions
def draw_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, color=(255, 255, 255), thickness=1):
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

def detect_fall(landmarks, image_height):
    left_shoulder_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_height)
    left_hip_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height)
    right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height)
    right_hip_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image_height)
    fall_threshold = 40
    return (
        left_hip_y - left_shoulder_y < fall_threshold or 
        right_hip_y - right_shoulder_y < fall_threshold
    )

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()



def generate_instructions():
    prompt = "A person has fallen and needs immediate help. Provide specific instructions."
    response = text_generator(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"].strip()

# API Endpoints

@app.post("/process/frame")
async def process_frame(file: UploadFile = File(...)):
    """
    Process a video frame to detect falls and distress signals.
    """
    try:
        # Read the uploaded file as an image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to RGB for Mediapipe processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
            results = pose.process(image)

        # Convert back to BGR for visualization
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            if detect_fall(landmarks, image.shape[0]):
                instruction_text = generate_instructions()
                speak(instruction_text)
                response_text = "Fall detected! Assistance instructions: " + instruction_text
            else:
                response_text = "No fall detected."
        else:
            response_text = "No landmarks detected."

        # Return response
        return {"message": response_text}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Welcome to the Fall Detection API!"}
