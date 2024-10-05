from strategies.exercise_strategy import ExerciseStrategy

class BenchPressStrategy(ExerciseStrategy):
    """
    Strategy for analyzing bench press.
    """

    def check_form(self, joint_angles, joint_distances):
        """
        Checks the bench press form based on elbow, shoulder, and wrist positions.
        """
        feedback = []

        # Ensure elbows are at the proper angle (between 70 and 90 degrees)
        if 'Right Elbow' in joint_angles and (joint_angles['Right Elbow'] < 70 or joint_angles['Right Elbow'] > 90):
            feedback.append("Keep your right elbow between 70 and 90 degrees for proper form.")

        if 'Left Elbow' in joint_angles and (joint_angles['Left Elbow'] < 70 or joint_angles['Left Elbow'] > 90):
            feedback.append("Keep your left elbow between 70 and 90 degrees for proper form.")

        # Check shoulder engagement
        if 'Right Shoulder Flexion' in joint_angles and joint_angles['Right Shoulder Flexion'] < 45:
            feedback.append("Ensure proper shoulder engagement on the right side.")

        if 'Left Shoulder Flexion' in joint_angles and joint_angles['Left Shoulder Flexion'] < 45:
            feedback.append("Ensure proper shoulder engagement on the left side.")

        return feedback
