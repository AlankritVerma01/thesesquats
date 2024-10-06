import numpy as np

def calculate_angle(point1, point2, point3):
    """
    Calculate the angle between three keypoints.
    The angle is calculated at point2, where vector1 = point1 - point2 and vector2 = point3 - point2.
    """
    try:
        p1, p2, p3 = np.array(point1), np.array(point2), np.array(point3)
        vector1 = p1 - p2
        vector2 = p3 - p2
        dot_product = np.dot(vector1, vector2)
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)
        # Prevent division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return None
        angle = np.arccos(dot_product / (magnitude1 * magnitude2))
        return np.degrees(angle)
    except Exception as e:
        # Handle exceptions such as invalid values
        return None

def is_valid_keypoint(keypoint):
    """
    Check if a keypoint is valid (not None and not zero).
    """
    if keypoint is None:
        return False
    x, y = keypoint[:2]
    return not (x == 0 and y == 0)

def calculate_joint_angles(keypoints):
    """
    Calculate angles for all key joints based on the detected keypoints.
    Returns a dictionary with joint names as keys and their calculated angles as values.
    """
    joint_angles = {}

    # Right Elbow (shoulder, elbow, wrist)
    if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[8]) and is_valid_keypoint(keypoints[10]):
        angle = calculate_angle(keypoints[6][:2], keypoints[8][:2], keypoints[10][:2])
        if angle is not None:
            joint_angles['Right Elbow'] = angle

    # Left Elbow (shoulder, elbow, wrist)
    if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[7]) and is_valid_keypoint(keypoints[9]):
        angle = calculate_angle(keypoints[5][:2], keypoints[7][:2], keypoints[9][:2])
        if angle is not None:
            joint_angles['Left Elbow'] = angle

    # Right Knee (hip, knee, ankle)
    if is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[14]) and is_valid_keypoint(keypoints[16]):
        angle = calculate_angle(keypoints[12][:2], keypoints[14][:2], keypoints[16][:2])
        if angle is not None:
            joint_angles['Right Knee'] = angle

    # Left Knee (hip, knee, ankle)
    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[13]) and is_valid_keypoint(keypoints[15]):
        angle = calculate_angle(keypoints[11][:2], keypoints[13][:2], keypoints[15][:2])
        if angle is not None:
            joint_angles['Left Knee'] = angle

    # Right Hip (shoulder, hip, knee)
    if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[14]):
        angle = calculate_angle(keypoints[6][:2], keypoints[12][:2], keypoints[14][:2])
        if angle is not None:
            joint_angles['Right Hip'] = angle

    # Left Hip (shoulder, hip, knee)
    if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[13]):
        angle = calculate_angle(keypoints[5][:2], keypoints[11][:2], keypoints[13][:2])
        if angle is not None:
            joint_angles['Left Hip'] = angle

    # Right Shoulder Flexion (hip, shoulder, elbow)
    if is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[8]):
        angle = calculate_angle(keypoints[12][:2], keypoints[6][:2], keypoints[8][:2])
        if angle is not None:
            joint_angles['Right Shoulder Flexion'] = angle

    # Left Shoulder Flexion (hip, shoulder, elbow)
    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[7]):
        angle = calculate_angle(keypoints[11][:2], keypoints[5][:2], keypoints[7][:2])
        if angle is not None:
            joint_angles['Left Shoulder Flexion'] = angle

    # Spine Angle (right shoulder, pelvis, left shoulder)
    if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[5]):
        angle = calculate_angle(keypoints[6][:2], keypoints[12][:2], keypoints[5][:2])
        if angle is not None:
            joint_angles['Spine Angle'] = angle

    # Right Ankle Dorsiflexion (knee, ankle, toes)
    # Add checks if you have toe keypoints; otherwise, comment out or adjust

    return joint_angles

def calculate_distance(point1, point2):
    """
    Calculates the Euclidean distance between two points (x, y).
    """
    p1, p2 = np.array(point1), np.array(point2)
    return np.linalg.norm(p1 - p2)

def calculate_joint_distances(keypoints):
    """
    Calculate the distances between key joints such as hip-shoulder width, shoulder-knee distance, etc.
    Useful for analyzing overall posture.
    """
    joint_distances = {}

    # Shoulder width (distance between left and right shoulder)
    if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[6]):
        distance = calculate_distance(keypoints[5][:2], keypoints[6][:2])
        joint_distances['Shoulder Width'] = distance

    # Hip width (distance between left and right hip)
    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[12]):
        distance = calculate_distance(keypoints[11][:2], keypoints[12][:2])
        joint_distances['Hip Width'] = distance

    # Spine length (distance between shoulders and pelvis)
    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[6]):
        spine_midpoint = (keypoints[5][:2] + keypoints[6][:2]) / 2
        pelvis_midpoint = (keypoints[11][:2] + keypoints[12][:2]) / 2
        distance = calculate_distance(spine_midpoint, pelvis_midpoint)
        joint_distances['Spine Length'] = distance

    return joint_distances
