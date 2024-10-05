pip install ultralytics


def get_model():
    return YOLO("yolo11n-pose.pt")


def get_pose(image_path):
    model = get_model()
    result = model(image_path)
    return result