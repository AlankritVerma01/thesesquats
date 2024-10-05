import streamlit as st
import cv2

st.title("TheSquats - Camera Feed")

# Initialize the camera
camera = cv2.VideoCapture(0)

# Create a placeholder in Streamlit for displaying the camera feed
stframe = st.empty()

st.write("Press 'q' in the terminal to stop the camera.")

# Continuously read frames from the camera
while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        st.write("Failed to capture video.")
        break

    # Display the camera feed in Streamlit
    stframe.image(frame, channels="BGR")

    # Stop the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera when done
camera.release()
cv2.destroyAllWindows()
