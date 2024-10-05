from angle_utils import calculate_joint_angles, calculate_joint_distances

class ExerciseStrategy:
    """
    Strategy interface that defines the common method for analyzing an exercise.
    """
    def analyze(self, keypoints):
        raise NotImplementedError("Subclasses must implement this method.")

class PullUpStrategy(ExerciseStrategy):
    """
    Concrete strategy for analyzing pull-ups.
    """
    def analyze(self, keypoints):
        feedback = []
        angles = calculate_joint_angles(keypoints)
        
        # Check elbow angle for pull-up
        if 'Right Elbow' in angles and angles['Right Elbow'] < 90:
            feedback.append("Pull-up: Right elbow bend is too shallow. Aim for a deeper bend.")

        if 'Left Elbow' in angles and angles['Left Elbow'] < 90:
            feedback.append("Pull-up: Left elbow bend is too shallow. Aim for a deeper bend.")
        
        # Check shoulder flexion
        if 'Right Shoulder Flexion' in angles and angles['Right Shoulder Flexion'] < 90:
            feedback.append("Pull-up: Improve right shoulder flexion for better movement.")
        
        # Additional checks for body posture, etc.
        return feedback

class BenchPressStrategy(ExerciseStrategy):
    """
    Concrete strategy for analyzing bench press.
    """
    def analyze(self, keypoints):
        feedback = []
        angles = calculate_joint_angles(keypoints)
        
        # Check elbow angle for proper range
        if 'Right Elbow' in angles and angles['Right Elbow'] < 60:
            feedback.append("Bench Press: Right elbow angle too small. Keep elbows at a 90-degree angle or wider.")

        if 'Left Elbow' in angles and angles['Left Elbow'] < 60:
            feedback.append("Bench Press: Left elbow angle too small. Keep elbows at a 90-degree angle or wider.")

        # Check for symmetrical shoulder flexion
        if 'Right Shoulder Flexion' in angles and 'Left Shoulder Flexion' in angles:
            if abs(angles['Right Shoulder Flexion'] - angles['Left Shoulder Flexion']) > 10:
                feedback.append("Bench Press: Shoulders are uneven. Try to balance the bar for an even press.")
        
        return feedback

class SquatStrategy(ExerciseStrategy):
    """
    Concrete strategy for analyzing squats.
    """
    def analyze(self, keypoints):
        feedback = []
        angles = calculate_joint_angles(keypoints)
        
        # Check knee angle for squat depth
        if 'Right Knee' in angles and angles['Right Knee'] < 80:
            feedback.append("Squat: Right knee angle too shallow. Aim for a deeper squat.")
        
        if 'Left Knee' in angles and angles['Left Knee'] < 80:
            feedback.append("Squat: Left knee angle too shallow. Aim for a deeper squat.")
        
        # Check hip angle for proper squat form
        if 'Right Hip' in angles and angles['Right Hip'] > 100:
            feedback.append("Squat: Right hip too extended. Maintain a neutral hip position.")
        
        return feedback
