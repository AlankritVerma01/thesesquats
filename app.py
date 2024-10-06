import streamlit as st
import cv2
import random
from utils.model_utils import get_model, get_keypoints_from_frame
from utils.angle_utils import calculate_joint_angles
from utils.video_utils import save_video, plot_joint_angles
from utils.exercise_rules import check_exercise_form, get_exercise_strategy
from utils.feedback_utils import FeedbackManager
from utils.chat_utils import get_ai_recommendation

# List of available exercises (strategies)
available_exercises = ['Pull-up', 'Squat', 'Bench Press', 'Easy Exercise']

# Load YOLO model
model = get_model()

# Instantiate feedback manager
feedback_manager = FeedbackManager()

# Initialize session state variables if not already initialized
if 'workout_started' not in st.session_state:
    st.session_state['workout_started'] = False
    st.session_state['current_exercise'] = 0
    st.session_state['custom_exercise'] = False
    st.session_state['workout_plan'] = []
    st.session_state['selected_exercise'] = None
    st.session_state['ai_conversation'] = ["Hey there! What do you want to work on today?"]
    st.session_state['exercise_mode'] = 'chat'  # 'chat', 'choose_own', 'upload_video'

# Start Workout Button
if st.button('Start Workout') and not st.session_state['workout_started']:
    st.session_state['workout_started'] = True

# Step 1: AI Chat Interaction
if st.session_state['workout_started']:

    if st.session_state['exercise_mode'] == 'chat':
        st.title("AI Workout Assistant")

        # Display AI conversation so far
        for message in st.session_state['ai_conversation']:
            st.write(f"AI: {message}")

        # Get user input and send to AI
        user_input = st.text_input("You:")
        if user_input:
            response = get_ai_recommendation(user_input)
            st.session_state['ai_conversation'].append(f"You: {user_input}")
            st.session_state['ai_conversation'].append(f"AI: {response['response']}")

            # Display AI response message
            st.write(response['response'])

            # Extract recommended exercise from the AI response
            if 'exercise' in response:
                st.session_state['recommended_exercise'] = response['exercise'].capitalize()
                st.write(f"AI Suggested Exercise: {st.session_state['recommended_exercise']}")

        # Option to follow AI or choose custom
        if st.session_state.get('recommended_exercise'):
            st.write("Would you like to follow the AI's recommendation or choose your own?")
            col1, col2 = st.columns(2)

            # Follow AI's recommendation
            with col1:
                if st.button(f"Do {st.session_state['recommended_exercise']}"):
                    if st.session_state['recommended_exercise'] in available_exercises:
                        st.session_state['selected_exercise'] = st.session_state['recommended_exercise']
                        st.session_state['exercise_mode'] = 'upload_video'  # Move to video upload
                    else:
                        st.write(f"The exercise '{st.session_state['recommended_exercise']}' is not in our database. Picking a random exercise.")
                        st.session_state['selected_exercise'] = random.choice(available_exercises)
                        st.write(f"Proceeding with {st.session_state['selected_exercise']}")
                        st.session_state['exercise_mode'] = 'upload_video'

            # Choose custom exercise
            with col2:
                if st.button("Choose my own exercise"):
                    # Stop the AI chat and move to exercise selection
                    st.session_state['custom_exercise'] = True
                    st.session_state['exercise_mode'] = 'choose_own'
                    st.stop()  # Immediately stop further execution to prevent chat from running

    # Custom exercise selection
    if st.session_state['exercise_mode'] == 'choose_own':
        st.write("Choose your own exercise from the list below:")
        st.session_state['selected_exercise'] = st.selectbox("Select an Exercise:", available_exercises)

        # Once exercise is selected, move to video upload
        if st.session_state['selected_exercise']:
            if st.button("Start Exercise"):
                st.session_state['exercise_mode'] = 'upload_video'

# Step 2: Video Upload and Exercise Analysis
if st.session_state['exercise_mode'] == 'upload_video' and st.session_state['selected_exercise']:
    st.write(f"Current Exercise: {st.session_state['selected_exercise']}")

    uploaded_video = st.file_uploader("Upload a video for analysis", type=["mp4", "avi", "mov"])

    if uploaded_video is not None:
        # Save uploaded video
        video_path = save_video(uploaded_video)

        cap = cv2.VideoCapture(video_path)
        stframe = st.empty()

        # Joint angle data storage
        joint_angle_data = {
            'Right Elbow': [], 'Left Elbow': [], 'Right Knee': [], 'Left Knee': [],
            'Right Hip': [], 'Left Hip': [], 'Right Shoulder Flexion': [], 'Left Shoulder Flexion': [],
            'Spine Angle': [], 'Right Ankle Dorsiflexion': [], 'Left Ankle Dorsiflexion': []
        }

        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        feedback_interval_seconds = 0.5
        feedback_frame_interval = int(frame_rate * feedback_interval_seconds)

        frame_count = 0
        last_feedback_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("Video ended or failed to read.")
                break

            keypoints = get_keypoints_from_frame(frame, model)
            if keypoints is not None:
                joint_angles = calculate_joint_angles(keypoints)

                for joint, angle in joint_angles.items():
                    joint_angle_data[joint].append(angle)

                if frame_count - last_feedback_frame >= feedback_frame_interval:
                    violations = check_exercise_form(st.session_state['selected_exercise'], joint_angles)
                    if violations:
                        st.write(f"Form Issues Detected: {violations}")
                    last_feedback_frame = frame_count

                annotated_frame = frame
                stframe.image(annotated_frame, channels="BGR")

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()

        # Plot joint angles over time
        st.write("### Joint Angles Over Time")
        for joint, angles in joint_angle_data.items():
            if any(angles):
                plot_joint_angles(angles, joint)

        # Show accumulated feedback at the end (optional)
        st.write("### Summary of All Form Feedback")
        st.write(feedback_manager.get_all_feedback())

        # After video analysis, return to chat for the next exercise
        if st.button("Next Exercise"):
            st.session_state['exercise_mode'] = 'chat'
            st.session_state['custom_exercise'] = False
            st.session_state['ai_conversation'] = ["Great job! Ready for the next exercise?"]

        if st.button("End Workout"):
            st.write("Workout Ended. Well done!")
            st.session_state.clear()
