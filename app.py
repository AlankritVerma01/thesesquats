import streamlit as st
import cv2
import random
import time  # For sleep in live video processing
from utils.model_utils import get_model, get_keypoints_from_frame
from utils.angle_utils import calculate_joint_angles, calculate_joint_distances
from utils.video_utils import save_video, plot_joint_angles
from utils.exercise_rules import check_exercise_form, get_exercise_strategy
from utils.feedback_utils import FeedbackManager
from utils.chat_utils import get_ai_recommendation
from utils.voice_utils import play_audio_feedback

# List of available exercises (strategies)
available_exercises = ['push-up', 'squat', 'bicep curl', 'lunge', 'overhead press', 'easy exercise']

# Load YOLO model
model = get_model()

# Initialize session state variables if not already initialized
def initialize_session_state():
    if 'workout_started' not in st.session_state:
        st.session_state['workout_started'] = False
        st.session_state['current_exercise'] = 0
        st.session_state['custom_exercise'] = False
        st.session_state['workout_plan'] = []
        st.session_state['selected_exercise'] = None
        st.session_state['ai_conversation'] = ["Hey there! What do you want to work on today?"]
        st.session_state['exercise_mode'] = 'chat'  # 'chat', 'choose_own', 'video_analysis'
        st.session_state['recommended_exercise'] = None
        st.session_state['feedback_manager'] = FeedbackManager()
        st.session_state['user_input'] = ''  # Initialize user_input
        st.session_state['ai_response'] = ''
        st.session_state['stop_live_exercise'] = False  # For stopping live exercise


# def play_audio_feedback(feedback):
#     if feedback and feedback != st.session_state['last_played_audio']:
#         audio_map = {
#             "Keep your back straight": "voice/sentence_13.mp3",
#             "Bend your knees more": "voice/sentence_14.mp3",
#             "Extend your arms fully": "voice/sentence_9.mp3",
#             "Right elbow not detected": "voice/sentence_9.mp3",
#             "Left elbow not detected": "voice/sentence_10.mp3",
#             # Add more mappings as needed
#         }
        
#         audio_file = audio_map.get(feedback)
#         if audio_file:
#             st.session_state['audio_placeholder'].empty()  # Clear previous audio
#             st.session_state['audio_placeholder'].audio(audio_file, format='audio/mp3')
#             st.session_state['last_played_audio'] = feedback

# Function to handle sending messages
def send_message():
    user_input = st.session_state['user_input']
    if user_input:
        st.session_state['ai_conversation'].append(f"You: {user_input}")
        try:
            response = get_ai_recommendation(user_input)
            ai_response = response.get('response', "Sorry, I didn't catch that.")
            st.session_state['ai_conversation'].append(f"AI: {ai_response}")
            st.session_state['ai_response'] = ai_response  # Store for displaying

            # Extract recommended exercise from the AI response
            if 'exercise' in response and response['exercise']:
                st.session_state['recommended_exercise'] = response['exercise'].capitalize()
            else:
                st.session_state['recommended_exercise'] = None
        except Exception as e:
            st.session_state['ai_conversation'].append("AI: Sorry, there was an error processing your request.")
            st.session_state['ai_response'] = "AI: Sorry, there was an error processing your request."
        # Clear the input field
        st.session_state['user_input'] = ''

def ai_chat_interaction():
    st.title("AI Workout Assistant")

    # Display AI conversation so far
    for message in st.session_state['ai_conversation']:
        st.write(message)

    # Get user input
    user_input = st.text_input("You:", key='user_input')

    # 'Send' button with callback
    st.button("Send", on_click=send_message, key='send_button')

    # Option to follow AI or choose custom
    if st.session_state.get('recommended_exercise'):
        st.write(f"AI Suggested Exercise: {st.session_state['recommended_exercise']}")
        st.write("Would you like to follow the AI's recommendation or choose your own?")
        col1, col2 = st.columns(2)

        # Follow AI's recommendation
        with col1:
            if st.button(f"Do {st.session_state['recommended_exercise']}", key='follow_ai'):
                if st.session_state['recommended_exercise'].lower() in available_exercises:
                    st.session_state['selected_exercise'] = st.session_state['recommended_exercise']
                    st.session_state['exercise_mode'] = 'video_analysis'  # Move to video analysis
                else:
                    st.write(f"The exercise '{st.session_state['recommended_exercise']}' is not in our database. Picking a random exercise.")
                    st.session_state['selected_exercise'] = random.choice(available_exercises)
                    st.write(f"Proceeding with {st.session_state['selected_exercise']}")
                    st.session_state['exercise_mode'] = 'video_analysis'

        # Choose custom exercise
        with col2:
            if st.button("Choose my own exercise", key='choose_own'):
                st.session_state['custom_exercise'] = True
                st.session_state['exercise_mode'] = 'choose_own'

# Custom Exercise Selection
def exercise_selection():
    st.write("Choose your own exercise from the list below:")
    selected_exercise = st.selectbox("Select an Exercise:", available_exercises, key='select_exercise')

    # Once exercise is selected, move to video analysis
    if st.button("Start Exercise", key='start_custom_exercise'):
        st.session_state['selected_exercise'] = selected_exercise
        st.session_state['exercise_mode'] = 'video_analysis'

def video_analysis():
    st.write(f"Current Exercise: {st.session_state['selected_exercise']}")

    # Reset the feedback manager at the start of a new analysis
    st.session_state['feedback_manager'].reset_feedback()

    # Option to choose input method
    input_method = st.radio("Choose Input Method:", ('Upload Video', 'Live Exercise'), key='input_method')

    if input_method == 'Upload Video':
        uploaded_video = st.file_uploader("Upload a video for analysis", type=["mp4", "avi", "mov"], key='video_uploader')
        if uploaded_video is not None:
            process_video(uploaded_video)
    elif input_method == 'Live Exercise':
        start_live_exercise = st.button("Start Live Exercise", key='start_live_exercise')
        if start_live_exercise:
            st.session_state['stop_live_exercise'] = False  # Reset the stop flag
            process_live_video()

def process_video(uploaded_video):
    # Save uploaded video
    video_path = save_video(uploaded_video)

    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()
    feedback_placeholder = st.empty()
    message_placeholder = st.empty()  # Add message placeholder

    # Joint angle data storage
    joint_angle_data = {joint: [] for joint in [
        'Right Elbow', 'Left Elbow', 'Right Knee', 'Left Knee',
        'Right Hip', 'Left Hip', 'Right Shoulder Flexion', 'Left Shoulder Flexion',
        'Spine Angle', 'Right Ankle Dorsiflexion', 'Left Ankle Dorsiflexion'
    ]}

    frame_rate = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 if frame rate is not available
    feedback_interval_seconds = 0.5
    feedback_frame_interval = int(frame_rate * feedback_interval_seconds)

    frame_count = 0
    last_feedback_frame = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("Video ended or failed to read.")
                break

            process_frame(frame, joint_angle_data, frame_count, last_feedback_frame, feedback_interval_seconds, feedback_placeholder, stframe, message_placeholder)
            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()

        # Post-processing steps
        post_exercise_analysis(joint_angle_data)

    except Exception as e:
        st.write(f"An error occurred during video processing: {e}")
        cap.release()
        cv2.destroyAllWindows()

def process_live_video():
    cap = cv2.VideoCapture(0)  # Capture from the webcam
    stframe = st.empty() 
    feedback_placeholder = st.empty()
    message_placeholder = st.empty()  # Add message placeholder

    # **Add a 'Stop' button**
    stop_button = st.button("Stop Live Exercise", key='stop_live_exercise_button')

    # Joint angle data storage
    joint_angle_data = {joint: [] for joint in [
        'Right Elbow', 'Left Elbow', 'Right Knee', 'Left Knee',
        'Right Hip', 'Left Hip', 'Right Shoulder Flexion', 'Left Shoulder Flexion',
        'Spine Angle', 'Right Ankle Dorsiflexion', 'Left Ankle Dorsiflexion'
    ]}

    frame_rate = 10  # Lower frame rate for processing
    feedback_interval_seconds = 0.5
    feedback_frame_interval = int(frame_rate * feedback_interval_seconds)

    frame_count = 0
    last_feedback_frame = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("Failed to capture frame from camera.")
                break

            # Flip the frame horizontally for a mirror effect
            frame = cv2.flip(frame, 1)

            process_frame(frame, joint_angle_data, frame_count, last_feedback_frame, feedback_frame_interval, feedback_placeholder, stframe, message_placeholder)
            frame_count += 1

            # Add a small delay
            time.sleep(1 / frame_rate)

            # Check if 'Stop' button is pressed
            if st.session_state.get('stop_live_exercise'):
                st.session_state['stop_live_exercise'] = False  # Reset the flag
                break

            # Check for 'Stop Live Exercise' button press
            if stop_button:
                st.session_state['stop_live_exercise'] = True

        cap.release()
        cv2.destroyAllWindows()

        # Post-processing steps
        post_exercise_analysis(joint_angle_data)

    except Exception as e:
        st.write(f"An error occurred during live video processing: {e}")
        cap.release()
        cv2.destroyAllWindows()

def process_frame(frame, joint_angle_data, frame_count, last_feedback_frame, feedback_frame_interval, feedback_placeholder, stframe, message_placeholder):
    keypoints, results = get_keypoints_from_frame(frame, model)
    if keypoints is not None and any(kp is not None for kp in keypoints):
        joint_angles = calculate_joint_angles(keypoints)
        joint_distances = calculate_joint_distances(keypoints)

        if joint_angles:
            message_placeholder.empty()

            for joint, angle in joint_angles.items():
                joint_angle_data[joint].append(angle)

            if frame_count - last_feedback_frame >= feedback_frame_interval:
                exercise_strategy = get_exercise_strategy(st.session_state['selected_exercise'])
                violations = exercise_strategy.check_form(joint_angles, joint_distances)

                current_feedback = st.session_state['feedback_manager'].update_feedback(violations)

                if current_feedback and current_feedback[0]:
                    latest_feedback = current_feedback[-1]
                    feedback_text = "Form Issue Detected:\n" + latest_feedback
                    feedback_placeholder.write(feedback_text)
                    play_audio_feedback(latest_feedback)  # Play audio feedback
                else:
                    feedback_placeholder.empty()
                    play_audio_feedback(None)  # Stop audio feedback

                last_feedback_frame = frame_count
        else:
            message_placeholder.write("Not enough keypoints detected to calculate joint angles.")
            feedback_placeholder.empty()

        if results is not None and len(results) > 0 and hasattr(results[0], 'plot'):
            annotated_frame = results[0].plot()
            annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            stframe.image(annotated_frame_bgr, channels="BGR")
        else:
            stframe.image(frame, channels="BGR")
    else:
        message_placeholder.write("No keypoints detected in the current frame.")
        stframe.image(frame, channels="BGR")
        feedback_placeholder.empty()

def post_exercise_analysis(joint_angle_data):
    # Plot joint angles over time
    st.write("### Joint Angles Over Time")
    for joint, angles in joint_angle_data.items():
        if any(angles):
            plot_joint_angles(angles, joint)

    # Show accumulated feedback at the end
    st.write("### Summary of All Form Feedback")
    all_feedback = st.session_state['feedback_manager'].get_all_feedback()
    if all_feedback:
        st.write(all_feedback)
    else:
        st.write("No form issues detected.")

    # After exercise, return to chat for the next exercise
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Exercise", key='next_exercise'):
            st.session_state['exercise_mode'] = 'chat'
            st.session_state['custom_exercise'] = False
            st.session_state['ai_conversation'] = ["Great job! Ready for the next exercise?"]
    with col2:
        if st.button("End Workout", key='end_workout'):
            st.write("Workout Ended. Well done!")
            st.session_state.clear()

# Function to start the workout
def start_workout():
    if st.button('Start Workout', key='start_workout') and not st.session_state['workout_started']:
        st.session_state['workout_started'] = True

# Main function to run the app
def main():
    initialize_session_state()
    start_workout()

    if st.session_state['workout_started']:
        if st.session_state['exercise_mode'] == 'chat':
            ai_chat_interaction()
        elif st.session_state['exercise_mode'] == 'choose_own':
            exercise_selection()
        elif st.session_state['exercise_mode'] == 'video_analysis' and st.session_state['selected_exercise']:
            video_analysis()

if __name__ == "__main__":
    main()
