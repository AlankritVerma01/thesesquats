import numpy as np
# Key Metrics Included:
# Elbow Angle: Measures flexion/extension of both elbows.
# Knee Angle: Measures flexion/extension of both knees.
# Hip Angle: Measures the angle at the hips, important for exercises like squats.
# Shoulder Flexion: Measures flexion at the shoulder joint.
# Spine Angle: Measures the alignment and curvature of the spine.
# Ankle Dorsiflexion: Measures the ankle movement, important for tracking squat depth or running posture.
# Joint Distances: Includes shoulder width, hip width, and spine length, which can help monitor posture during exercises.

def calculate_angle(point1, point2, point3):
    """
    Calculate the angle between three keypoints.
    Points should be in the format (x, y) representing the keypoint locations.
    The angle is calculated at point2, where vector1 = point1 - point2 and vector2 = point3 - point2.
    """
    p1, p2, p3 = np.array(point1), np.array(point2), np.array(point3)
    vector1 = p1 - p2
    vector2 = p3 - p2
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    angle = np.arccos(dot_product / (magnitude1 * magnitude2))
    return np.degrees(angle)

def is_valid_keypoint(keypoint):
    """
    Check if a keypoint is valid (not zero).
    The keypoint is valid if it's not (0, 0), which indicates it's not detected.
    """
    return not (keypoint[0] == 0 and keypoint[1] == 0)

def calculate_joint_angles(keypoints):
    """
    Calculate angles for all key joints based on the detected keypoints.
    Returns a dictionary with joint names as keys and their calculated angles as values.
    """
    joint_angles = {}

    # Right Elbow (shoulder, elbow, wrist)
    if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[8]) and is_valid_keypoint(keypoints[10]):
        joint_angles['Right Elbow'] = calculate_angle(keypoints[6][:2], keypoints[8][:2], keypoints[10][:2])

    # Left Elbow (shoulder, elbow, wrist)
    if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[7]) and is_valid_keypoint(keypoints[9]):
        joint_angles['Left Elbow'] = calculate_angle(keypoints[5][:2], keypoints[7][:2], keypoints[9][:2])

    # Right Knee (hip, knee, ankle)
    if is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[14]) and is_valid_keypoint(keypoints[16]):
        joint_angles['Right Knee'] = calculate_angle(keypoints[12][:2], keypoints[14][:2], keypoints[16][:2])

    # Left Knee (hip, knee, ankle)
    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[13]) and is_valid_keypoint(keypoints[15]):
        joint_angles['Left Knee'] = calculate_angle(keypoints[11][:2], keypoints[13][:2], keypoints[15][:2])

    # Right Hip (shoulder, hip, knee)
    if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[14]):
        joint_angles['Right Hip'] = calculate_angle(keypoints[6][:2], keypoints[12][:2], keypoints[14][:2])

    # Left Hip (shoulder, hip, knee)
    if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[13]):
        joint_angles['Left Hip'] = calculate_angle(keypoints[5][:2], keypoints[11][:2], keypoints[13][:2])

    # Shoulder Flexion (hip, shoulder, elbow)
    if is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[8]):
        joint_angles['Right Shoulder Flexion'] = calculate_angle(keypoints[12][:2], keypoints[6][:2], keypoints[8][:2])

    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[7]):
        joint_angles['Left Shoulder Flexion'] = calculate_angle(keypoints[11][:2], keypoints[5][:2], keypoints[7][:2])

    # Spine Angle (right shoulder, pelvis, left shoulder)
    if is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[11]):
        joint_angles['Spine Angle'] = calculate_angle(keypoints[6][:2], keypoints[12][:2], keypoints[11][:2])

    # Ankle Dorsiflexion (knee, ankle, toes)
    if is_valid_keypoint(keypoints[14]) and is_valid_keypoint(keypoints[16]) and is_valid_keypoint(keypoints[20]):
        joint_angles['Right Ankle Dorsiflexion'] = calculate_angle(keypoints[14][:2], keypoints[16][:2], keypoints[20][:2])

    if is_valid_keypoint(keypoints[13]) and is_valid_keypoint(keypoints[15]) and is_valid_keypoint(keypoints[19]):
        joint_angles['Left Ankle Dorsiflexion'] = calculate_angle(keypoints[13][:2], keypoints[15][:2], keypoints[19][:2])

    return joint_angles

def calculate_distance(point1, point2):
    """Calculates the Euclidean distance between two points (x, y)."""
    p1, p2 = np.array(point1), np.array(point2)
    return np.linalg.norm(p1 - p2)

def calculate_joint_distances(keypoints):
    """
    Calculate the distances between key joints that might be useful for analysis,
    such as hip-shoulder width, shoulder-knee distance, etc.
    """
    joint_distances = {}

    # Shoulder width (distance between left and right shoulder)
    if is_valid_keypoint(keypoints[5]) and is_valid_keypoint(keypoints[6]):
        joint_distances['Shoulder Width'] = calculate_distance(keypoints[5][:2], keypoints[6][:2])

    # Hip width (distance between left and right hip)
    if is_valid_keypoint(keypoints[11]) and is_valid_keypoint(keypoints[12]):
        joint_distances['Hip Width'] = calculate_distance(keypoints[11][:2], keypoints[12][:2])

    # Spine length (distance between shoulders and pelvis)
    if is_valid_keypoint(keypoints[12]) and is_valid_keypoint(keypoints[6]) and is_valid_keypoint(keypoints[11]):
        spine_midpoint = ((keypoints[12][:2] + keypoints[11][:2]) / 2)
        joint_distances['Spine Length'] = calculate_distance(spine_midpoint, keypoints[12][:2])

    return joint_distances
