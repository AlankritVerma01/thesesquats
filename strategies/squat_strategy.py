from strategies.exercise_strategy import ExerciseStrategy

class SquatStrategy(ExerciseStrategy):
    """
    Strategy for analyzing squats.
    """

    def check_form(self, joint_angles, joint_distances):
        """
        Checks the squat form based on the knee, hip, and ankle angles.
        """
        feedback = []

        # Check if knees are bending properly
        if 'Right Knee' in joint_angles and joint_angles['Right Knee'] > 160:
            feedback.append("Bend your right knee more to get full depth on the squat.")

        if 'Left Knee' in joint_angles and joint_angles['Left Knee'] > 160:
            feedback.append("Bend your left knee more to get full depth on the squat.")

        # Check if hips are lowering sufficiently (hip angles)
        if 'Right Hip' in joint_angles and joint_angles['Right Hip'] > 90:
            feedback.append("Lower your right hip to get deeper in the squat.")

        if 'Left Hip' in joint_angles and joint_angles['Left Hip'] > 90:
            feedback.append("Lower your left hip to get deeper in the squat.")

        # Check ankle dorsiflexion for flexibility (should be less than a certain angle)
        if 'Right Ankle Dorsiflexion' in joint_angles and joint_angles['Right Ankle Dorsiflexion'] < 10:
            feedback.append("Improve ankle mobility for a better squat depth (Right).")

        if 'Left Ankle Dorsiflexion' in joint_angles and joint_angles['Left Ankle Dorsiflexion'] < 10:
            feedback.append("Improve ankle mobility for a better squat depth (Left).")

        return feedback
