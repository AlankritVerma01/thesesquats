import streamlit as st
import cv2
import numpy as np
from yolo_model.model import get_pose


st.title("TheSquats - Camera Feed")

# Initialize the camera
camera = cv2.VideoCapture(0)

# Create a placeholder in Streamlit for displaying the camera feed
stframe = st.empty()

st.write("Press 'q' in the terminal to stop the camera.")

while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        st.write("Failed to capture video.")
        break
    
    # Convert the frame to RGB (YOLO expects RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Perform pose detection
    results = get_pose(frame_rgb)
    # Draw the pose detection results on the frame
    annotated_frame = results[0].plot()
    
    # Convert the annotated frame back to BGR for display
    annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
    
    # Display the annotated camera feed in Streamlit
    stframe.image(annotated_frame_bgr, channels="BGR")
    
    # Stop the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera when done
camera.release()
cv2.destroyAllWindows()