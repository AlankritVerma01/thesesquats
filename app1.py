import streamlit as st
import cv2
import numpy as np
from yolo_model.model import get_model  # Assuming you have the model defined here
from ultralytics.solutions import AIGym
import math

# Load the YOLO model
model = get_model()

# Monitor arm bending based on elbow angle
class ArmBendMonitor:
    def __init__(self):
        self.bend_count = 0
        self.is_bent = False

    def calculate_angle(self, point1, point2, point3):
        """Calculate the angle between three points (e.g., shoulder, elbow, wrist)."""
        p1, p2, p3 = np.array(point1), np.array(point2), np.array(point3)
        vector1 = p1 - p2
        vector2 = p3 - p2
        dot_product = np.dot(vector1, vector2)
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)
        angle = np.arccos(dot_product / (magnitude1 * magnitude2))
        return np.degrees(angle)

    def monitor_arm_bend(self, keypoints):
        """Attempt to monitor arm bending based on keypoints for shoulder, elbow, wrist."""
        # Print all the keypoints to inspect their structure
        print("All keypoints:", keypoints)

        # For now, we're just printing everything
        try:
            # Let's print everything and inspect the result structure
            for i, keypoint in enumerate(keypoints):
                print(f"Keypoint {i}: {keypoint}")

            # Attempt to extract keypoints for left arm (shoulder, elbow, wrist)
            shoulder = keypoints[5][:2]
            elbow = keypoints[7][:2]
            wrist = keypoints[9][:2]

            # Print these specific keypoints for arm monitoring
            print(f"Shoulder: {shoulder}, Elbow: {elbow}, Wrist: {wrist}")

            # Calculate the elbow angle
            angle = self.calculate_angle(shoulder, elbow, wrist)
            print(f"Elbow angle: {angle}")

            return angle, self.bend_count
        except IndexError:
            print("Not enough keypoints detected for arm bend monitoring.")
            return None, self.bend_count

# Streamlit UI
st.title("Real-Time Arm Bend Monitoring")

# Initialize camera
camera = cv2.VideoCapture(0)
stframe = st.empty()

# Create arm bend monitor instance
arm_bend_monitor = ArmBendMonitor()

while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        st.write("Failed to capture video.")
        break

    # Convert frame to RGB for YOLO model input
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform pose detection using YOLO model loaded with get_model()
    results = model(frame_rgb)

    # Print the entire result structure to inspect it
    print("Results object:", results)

    if results and results[0].keypoints is not None:
        keypoints = results[0].keypoints

        # Monitor arm bending based on keypoints
        angle, bend_count = arm_bend_monitor.monitor_arm_bend(keypoints)

        # Display feedback on the screen
        if angle is not None:
            st.write(f"Elbow Angle: {int(angle)} degrees")
            st.write(f"Arm Bend Count: {bend_count}")

        # Annotate the frame with keypoints
        annotated_frame = results[0].plot()

        # Convert back to BGR for display
        annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
        stframe.image(annotated_frame_bgr, channels="BGR")
    
    # Stop the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()
