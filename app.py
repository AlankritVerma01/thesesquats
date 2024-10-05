import streamlit as st
import cv2
from utils.model_utils import get_model, get_keypoints_from_frame
from utils.angle_utils import calculate_joint_angles
from utils.video_utils import save_video, plot_joint_angles
from utils.exercise_rules import check_exercise_form
from utils.feedback_utils import FeedbackManager  # Import the feedback manager

# Load YOLO model
model = get_model()
 
# Instantiate feedback manager
feedback_manager = FeedbackManager()

# Streamlit UI
st.title("Comprehensive Joint Monitoring and Exercise Form Analysis")

# Select exercise type
exercise_type = st.selectbox("Select an exercise for analysis", ['Pull-up', 'Squat', 'Bench Press', 'Easy Exercise'])

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
        'Right Shoulder Flexion': [],
        'Left Shoulder Flexion': [],
        'Spine Angle': [],
        'Right Ankle Dorsiflexion': [],
        'Left Ankle Dorsiflexion': []
    }

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
            joint_angles = calculate_joint_angles(keypoints)

            # Update joint angle data for the video
            for joint, angle in joint_angles.items():
                joint_angle_data[joint].append(angle)

            # Check if the current frame meets exercise form rules using exercise_rules utility
            feedback = check_exercise_form(exercise_type, joint_angles)

            # Process and display feedback
            if feedback:
                processed_feedback = feedback_manager.process_feedback(feedback)
                st.write(f"Form Issues Detected: {processed_feedback}")

            # Display annotated frame (You can add annotations if needed)
            stframe.image(frame, channels="BGR")

    # Release video resources
    cap.release()
    cv2.destroyAllWindows()

    # Plot the joint angles over the video timeline
    st.write("### Joint Angles Over Time")
    for joint, angles in joint_angle_data.items():
        if any(angles):
            plot_joint_angles(angles, joint)

    # Display all accumulated feedback at the end (optional)
    st.write("### Summary of All Form Feedback")
    st.write(feedback_manager.get_all_feedback())
