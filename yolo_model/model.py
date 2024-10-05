from ultralytics import YOLO

def get_model():
    return YOLO("yolo11n-pose.pt")


def get_pose(image_path):
    model = get_model()
    result = model.predict(source = image_path)
    return result, get_feedback(result)# , exercise)

def get_feedback(result):#, exercise):
    return "feedback"