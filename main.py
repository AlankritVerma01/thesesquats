import streamlit as st

st.title("TheSquats - AI Gym Assistant")
st.write("Upload a video of your workout to check your exercise form.")

# User selects exercise
exercise_name = st.selectbox("Choose your exercise", ["Squat", "Push-ups", "Deadlift"])

# Upload workout video
uploaded_video = st.file_uploader("Upload your workout video", type=["mp4", "avi"])

if uploaded_video:
    st.write("Processing the video...")

    # Process the uploaded video to get the user's vectors
    user_vectors = process_video(uploaded_video)

    # Fetch the correct vectors from MongoDB
    correct_vectors = fetch_correct_vectors(exercise_name)

    # Compare user vectors with correct vectors
    feedback = compare_vectors(user_vectors, correct_vectors)

    # Display feedback to the user
    st.subheader("Feedback")
    for error in feedback:
        st.write(error)
