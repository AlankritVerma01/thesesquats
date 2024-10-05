import streamlit as st
import cv2
import numpy as np
from yolo_model.model import get_pose
import random
import pyttsx3
import time
from PIL import Image
import math

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Sample data (you can expand this)
routines = {
    "Full Body Workout": ["Squats", "Push-ups", "Lunges", "Plank"],
    "Upper Body Focus": ["Push-ups", "Pull-ups", "Shoulder Press", "Bicep Curls"],
    "Lower Body Focus": ["Squats", "Lunges", "Deadlifts", "Calf Raises"]

st.title("TheSquats - Camera Feed with Keypoint Inspection")

motivational_quotes = [
    "You're doing great! Keep pushing!",
    "Every rep counts. You've got this!",
    "Stay strong, stay focused!",
    "Pain is temporary, pride is forever!",
    "You're stronger than you think!"
]

# Add placeholder images for each routine
routine_images = {
    "Full Body Workout": "https://example.com/full_body.jpg",
    "Upper Body Focus": "https://example.com/upper_body.jpg",
    "Lower Body Focus": "https://example.com/lower_body.jpg"
}

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

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

def main_page():
    st.set_page_config(page_title="TheSquats - Gym Routine App", layout="wide")
    
    st.title("TheSquats - Gym Routine App")
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .stSelectbox>div>div>select {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
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
    
    with col1:
        st.markdown('<p class="big-font">Choose Your Routine</p>', unsafe_allow_html=True)
        selected_routine = st.selectbox("", list(routines.keys()) + ["Custom routine"])
        
        if selected_routine == "Custom routine":
            selected_exercises = st.multiselect("Select exercises for your custom routine:", 
                                                set([exercise for routine in routines.values() for exercise in routine]))
            if selected_exercises:
                routines["Custom"] = selected_exercises
            else:
                st.warning("Please select at least one exercise for your custom routine.")
                return
    
    with col2:
        if selected_routine in routine_images:
            st.image(routine_images[selected_routine], use_column_width=True)
        else:
            st.image("https://example.com/custom_routine.jpg", use_column_width=True)
    
    if st.button("Start Workout", key="start_workout"):
        st.session_state.routine = routines[selected_routine]
        st.session_state.current_exercise = 0
        st.session_state.current_set = 1
        st.session_state.page = "exercise_intro"

def exercise_intro_page():
    exercise = st.session_state.routine[st.session_state.current_exercise]
    st.title(f"Get Ready for {exercise}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Here you would embed a video of the exercise
        st.video("https://example.com/exercise_video.mp4")
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
            <h2>Exercise: {exercise}</h2>
            <p>Set: {st.session_state.current_set}/3</p>
            <p>Duration: 30 seconds</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Exercise", key="start_exercise"):
            st.session_state.page = "camera_feed"

def camera_feed_page():
    exercise = st.session_state.routine[st.session_state.current_exercise]
    st.title(f"{exercise} - Set {st.session_state.current_set}")

    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise ValueError("Could not open camera. Please check your camera connection.")

        stframe = st.empty()

        start_time = time.time()
        duration = 30  # Exercise duration in seconds

        while (time.time() - start_time) < duration:
            ret, frame = camera.read()
            if not ret:
                st.write("Failed to capture video frame.")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results, feedback = get_pose(frame_rgb)
            annotated_frame = results[0].plot()
            
            stframe.image(annotated_frame, channels="RGB")
            
            if feedback:
                text_to_speech(feedback)

        camera.release()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please make sure your camera is connected and not being used by another application.")
    
    finally:
        st.session_state.page = "set_complete"

def set_complete_page():
    st.title("Set Complete!")
    quote = random.choice(motivational_quotes)
    
    st.markdown(f"""
    <div style="background-color: #e6f3ff; padding: 20px; border-radius: 10px; text-align: center;">
        <h2>{quote}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    text_to_speech(quote)

    col1, col2 = st.columns(2)

    if st.session_state.current_set < 3:  # Assuming 3 sets per exercise
        if col1.button("Next Set", key="next_set"):
            st.session_state.current_set += 1
            st.session_state.page = "exercise_intro"
    else:
        if st.session_state.current_exercise < len(st.session_state.routine) - 1:
            if col1.button("Next Exercise", key="next_exercise"):
                st.session_state.current_exercise += 1
                st.session_state.current_set = 1
                st.session_state.page = "exercise_intro"
        else:
            if col1.button("Finish Workout", key="finish_workout"):
                st.session_state.page = "workout_complete"
    
    if col2.button("Back to Main Menu", key="back_to_main"):
        st.session_state.page = "main"

def workout_complete_page():
    st.balloons()
    st.title("Congratulations!")
    st.markdown("""
    <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center;">
        <h2>You've completed your workout. Great job!</h2>
    </div>
    """, unsafe_allow_html=True)
    text_to_speech("Congratulations! You've completed your workout. Great job!")

    if st.button("Back to Main Menu", key="back_to_main_complete"):
        st.session_state.page = "main"

def app():
    if 'page' not in st.session_state:
        st.session_state.page = "main"

    pages = {
        "main": main_page,
        "exercise_intro": exercise_intro_page,
        "camera_feed": camera_feed_page,
        "set_complete": set_complete_page,
        "workout_complete": workout_complete_page
    }

    pages[st.session_state.page]()

if __name__ == "__main__":
    app()