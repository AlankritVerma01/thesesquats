import streamlit as st
import cv2
import numpy as np
from yolo_model.model import get_pose
import math

st.title("TheSquats - Camera Feed with Keypoint Inspection")

# Initialize the camera
camera = cv2.VideoCapture(0)

# Create a placeholder in Streamlit for displaying the camera feed
stframe = st.empty()

def calculate_angle(point1, point2, point3):
    """Calculate the angle between three points (shoulder, elbow, wrist)."""
    p1 = np.array(point1)  # Shoulder
    p2 = np.array(point2)  # Elbow
    p3 = np.array(point3)  # Wrist

    vector1 = p1 - p2  # Shoulder to Elbow
    vector2 = p3 - p2  # Wrist to Elbow

    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    angle = np.arccos(dot_product / (magnitude1 * magnitude2))
    return np.degrees(angle)

while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        st.write("Failed to capture video.")
        break
    
    # Convert the frame to RGB (YOLO expects RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Perform pose detection
    results = get_pose(frame_rgb)

    if results and results[0].keypoints is not None:
        keypoints = results[0].keypoints

        # Print keypoints to inspect their structure
        st.write(f"Detected keypoints: {keypoints}")

        # Optionally, visualize the keypoints by printing them out in a structured way
        for i, keypoint in enumerate(keypoints):
            # Ensure the keypoint has at least 2 values (x, y) and optionally 3 (confidence)
            if len(keypoint) >= 2:
                x, y = keypoint[:2]
                confidence = keypoint[2] if len(keypoint) > 2 else None
                st.write(f"Keypoint {i}: (x: {x}, y: {y}), Confidence: {confidence if confidence else 'N/A'}")
            else:
                st.write(f"Keypoint {i}: Not enough data to display (keypoint data: {keypoint})")
        
        # Example of extracting shoulder, elbow, and wrist points (for arm analysis)
        try:
            shoulder = keypoints[5][:2]  # Left shoulder
            elbow = keypoints[7][:2]     # Left elbow
            wrist = keypoints[9][:2]     # Left wrist

            # Calculate the arm angle
            angle = calculate_angle(shoulder, elbow, wrist)
            st.write(f"Arm angle: {angle} degrees")

        except IndexError:
            st.write("Not enough keypoints to analyze the arm pose.")
    
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
