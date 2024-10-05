import cv2
from yolo_model.model import get_model  # Your model loading function

def get_model():
    """Loads the YOLO model."""
    return get_model()

def get_keypoints_from_frame(frame, model):
    """Uses the YOLO model to get keypoints from the frame."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)

    if results and results[0].keypoints is not None:
        keypoints = results[0].keypoints.data[0]
        return keypoints
    return None
