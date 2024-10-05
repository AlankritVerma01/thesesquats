import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from utils.pose_estimation import process_video, process_camera
from utils.mongodb import fetch_correct_vectors
from utils.comparison import compare_vectors
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb+srv://username:password@cluster0.mongodb.net/thesquats_db?retryWrites=true&w=majority")
db = client["thesquats_db"]
collection = db["exercises"]

# Load YOLO model
model = YOLO("yolo_model/yolo11n-pose.pt")

st.title("TheSquats - AI Gym Assistant")
st.write("Upload a video or use your camera to check your exercise form.")

# Select exercise
exercise_name = st.selectbox("Choose your exercise", ["Squat", "Push-ups", "Deadlift"])

# Choose between video upload or camera
input_method = st.radio("Choose input method", ("Upload Video", "Use Camera"))

if input_method == "Upload Video":
    # Upload video
    uploaded_video = st.file_uploader("Upload your workout video", type=["mp4", "avi"])

    if uploaded_video:
        st.write("Processing the video...")

        # Process video for pose estimation
        user_vectors = process_video(uploaded_video, model)

        # Fetch correct vectors from MongoDB
        correct_vectors = fetch_correct_vectors(exercise_name, collection)

        # Compare vectors and give feedback
        feedback = compare_vectors(user_vectors, correct_vectors)
        
        st.subheader("Feedback")
        for error in feedback:
            st.write(error)

elif input_method == "Use Camera":
    # Camera integration
    camera = cv2.VideoCapture(0)
    
    stframe = st.empty()
    st.write("Press 'q' to stop the camera.")
    
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break
        
        # Process camera frame for pose estimation
        user_vectors = process_camera(frame, model)
        
        # Fetch correct vectors from MongoDB
        correct_vectors = fetch_correct_vectors(exercise_name, collection)
        
        # Compare vectors and give feedback on the fly (optional)
        feedback = compare_vectors(user_vectors, correct_vectors)
        stframe.image(frame, channels="BGR")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

# Sidebar for additional features like workout schedules and guide videos
st.sidebar.title("Gym Features")
schedule = st.sidebar.selectbox("Choose your workout schedule", ["Beginner", "Intermediate", "Advanced"])
st.sidebar.video("https://www.youtube.com/watch?v=example_squat_guide")
