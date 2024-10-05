import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from yolo_model.model import get_model  # Assuming you have the model defined here
import math

# Load the YOLO model
model = get_model()

# Function to calculate the angle between three keypoints
def calculate_angle(point1, point2, point3):
    """Calculate the angle between three points (e.g., shoulder, elbow, wrist)."""
    p1, p2, p3 = np.array(point1), np.array(point2), np.array(point3)
    vector1 = p1 - p2
    vector2 = p3 - p2
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    angle = np.arccos(dot_product / (magnitude1 * magnitude2))
    return np.degrees(angle)

# Function to check if a keypoint is valid (not zero)
def is_valid_keypoint(keypoint):
    """Check if a keypoint is valid (not zero)."""
    return not (keypoint[0] == 0 and keypoint[1] == 0)

# Function to plot joint angle data
def plot_joint_angle(joint_angles, joint_name):
    """Generate a plot for a specific joint angle over time."""
    plt.figure()
    plt.plot(joint_angles, label=f"{joint_name} Angle")
    plt.xlabel("Frame Number")
    plt.ylabel("Angle (degrees)")
    plt.title(f"{joint_name} Angle Over Time")
    plt.legend()
    st.pyplot(plt)

# Streamlit UI
st.title("Full-Body Joint Monitoring and Video Annotation")

# Upload video file
uploaded_video = st.file_uploader("Upload a video for analysis", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    # Save uploaded video temporarily
    video_path = f"temp_video.{uploaded_video.name.split('.')[-1]}"
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
    
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()

    # Dictionary to store joint angles for the entire video
    joint_angle_data = {
        'Right Elbow': [],
        'Left Elbow': [],
        'Right Knee': [],
        'Left Knee': []
    }

    frame_count = 0  # Keep track of frames

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Video ended or failed to read the video.")
            break

        # Convert frame to RGB for YOLO model input
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform pose detection using YOLO model
        results = model(frame_rgb)

        if results and results[0].keypoints is not None:
            keypoints = results[0].keypoints.data[0]  # Access keypoints data

            # Joint analysis
            angles = {}

            # Right Elbow (shoulder, elbow, wrist)
            if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[8]) and is_valid_keypoint(keypoints[10]):
                right_elbow_angle = calculate_angle(keypoints[6][:2], keypoints[8][:2], keypoints[10][:2])
                angles['Right Elbow'] = right_elbow_angle
                joint_angle_data['Right Elbow'].append(right_elbow_angle)
            else:
                joint_angle_data['Right Elbow'].append(None)

            # Left Elbow (shoulder, elbow, wrist)
            if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[7]) and is_valid_keypoint(keypoints[9]):
                left_elbow_angle = calculate_angle(keypoints[5][:2], keypoints[7][:2], keypoints[9][:2])
                angles['Left Elbow'] = left_elbow_angle
                joint_angle_data['Left Elbow'].append(left_elbow_angle)
            else:
                joint_angle_data['Left Elbow'].append(None)

            # Right Knee (hip, knee, ankle)
            if is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[14]) and is_valid_keypoint(keypoints[16]):
                right_knee_angle = calculate_angle(keypoints[12][:2], keypoints[14][:2], keypoints[16][:2])
                angles['Right Knee'] = right_knee_angle
                joint_angle_data['Right Knee'].append(right_knee_angle)
            else:
                joint_angle_data['Right Knee'].append(None)

            # Left Knee (hip, knee, ankle)
            if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[13]) and is_valid_keypoint(keypoints[15]):
                left_knee_angle = calculate_angle(keypoints[11][:2], keypoints[13][:2], keypoints[15][:2])
                angles['Left Knee'] = left_knee_angle
                joint_angle_data['Left Knee'].append(left_knee_angle)
            else:
                joint_angle_data['Left Knee'].append(None)

            # Annotate the frame with keypoints and angles
            annotated_frame = results[0].plot()

            # Convert back to BGR for display
            annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            stframe.image(annotated_frame_bgr, channels="BGR")

            frame_count += 1  # Increment frame count

    # Release video resources
    cap.release()
    cv2.destroyAllWindows()

    # Generate graphs for each joint angle after the video is processed
    st.write("### Joint Angles Over Time")

    # Plot the angles for each joint
    if joint_angle_data['Right Elbow']:
        plot_joint_angle(joint_angle_data['Right Elbow'], 'Right Elbow')
    if joint_angle_data['Left Elbow']:
        plot_joint_angle(joint_angle_data['Left Elbow'], 'Left Elbow')
    if joint_angle_data['Right Knee']:
        plot_joint_angle(joint_angle_data['Right Knee'], 'Right Knee')
    if joint_angle_data['Left Knee']:
        plot_joint_angle(joint_angle_data['Left Knee'], 'Left Knee')

