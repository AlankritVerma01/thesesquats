import streamlit as st
import cv2
from utils.model_utils import get_model, get_keypoints_from_frame
from utils.angle_utils import calculate_joint_angles
from utils.exercise_rules import check_exercise_form
from utils.video_utils import save_video, plot_joint_angles

# Load YOLO model
model = get_model()

# Streamlit UI
st.title("Comprehensive Joint Monitoring and Exercise Form Analysis")

# Upload video file
uploaded_video = st.file_uploader("Upload a video for analysis", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    # Save uploaded video temporarily
    video_path = save_video(uploaded_video)

    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()

    # Dictionary to store joint angles for the entire video
    joint_angle_data = {
        'Right Elbow': [],
        'Left Elbow': [],
        'Right Knee': [],
        'Left Knee': [],
        'Right Hip': [],
        'Left Hip': [],
        'Shoulder Flexion': [],
        'Spine Angle': [],
        'Ankle Dorsiflexion': []
    }

    frame_count = 0  # Keep track of frames

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Video ended or failed to read the video.")
            break

        # Process each frame and extract keypoints
        keypoints = get_keypoints_from_frame(frame, model)

        # If keypoints are detected
        if keypoints is not None:
            # Calculate angles for key joints
            angles = calculate_joint_angles(keypoints)

            # Update joint angle data for the video
            for joint, angle in angles.items():
                joint_angle_data[joint].append(angle)

            # Check if the current frame meets exercise form rules
            violations = check_exercise_form(angles)

            # Display feedback based on the rules
            if violations:
                st.write(f"Form Issues Detected: {violations}")

            # Annotate and display frame with feedback
            annotated_frame = frame  # You can implement this function to draw feedback on the frame
            stframe.image(annotated_frame, channels="BGR")

            frame_count += 1

    # Release video resources
    cap.release()
    cv2.destroyAllWindows()

    # Plot the joint angles over the video timeline
    st.write("### Joint Angles Over Time")
    for joint, angles in joint_angle_data.items():
        if any(angles):
            plot_joint_angles(angles, joint)
