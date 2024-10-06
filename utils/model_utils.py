import cv2
from yolo_model.model import get_model_yolo  # Your model loading function
import numpy as np

def get_model():
    """Loads the YOLO model."""
    return get_model_yolo()

def get_keypoints_from_frame(frame, model):
    """Uses the YOLO model to get keypoints from the frame."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)

    if results is not None and len(results) > 0 and results[0].keypoints is not None:
        keypoints_data = results[0].keypoints.data[0]  # Assuming single person detection
        num_keypoints = keypoints_data.shape[0]

        # Expected number of keypoints based on your model (e.g., 17 for COCO)
        expected_num_keypoints = 20  # Adjust based on your model

        # Initialize keypoints array with None
        keypoints = [None] * expected_num_keypoints

        # Fill in detected keypoints
        for idx in range(min(num_keypoints, expected_num_keypoints)):
            keypoints[idx] = keypoints_data[idx]
        # print("Detected keypoints:", keypoints_data)
        return keypoints, results
    else:
        # Return an array of Nones if no keypoints are detected
        expected_num_keypoints = 20  # Adjust based on your model
        keypoints = [None] * expected_num_keypoints
        return keypoints, results  # Return results even if None
