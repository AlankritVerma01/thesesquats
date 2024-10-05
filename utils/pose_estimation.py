import cv2
from ultralytics import YOLO

def process_video(video_path, model):
    video = cv2.VideoCapture(video_path)
    user_vectors = []

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        # Pose estimation using YOLO
        results = model(frame)

        # Collect keypoints (vectors)
        for person in results.xy:
            keypoints = person['keypoints']
            user_vectors.append(keypoints)

    video.release()
    return user_vectors

def process_camera(frame, model):
    # Pose estimation using YOLO for live camera feed
    user_vectors = []

    results = model(frame)

    for person in results.xy:
        keypoints = person['keypoints']
        user_vectors.append(keypoints)

    return user_vectors
