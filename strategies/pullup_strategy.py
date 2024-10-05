from strategies.exercise_strategy import ExerciseStrategy

class PullUpStrategy(ExerciseStrategy):
    """
    Strategy for analyzing pull-ups.
    """

    def check_form(self, joint_angles, joint_distances):
        """
        Checks the pull-up form based on the elbow, shoulder, and other relevant joint angles.
        """
        feedback = []

        # Check if elbows are fully extended at the bottom of the pull-up
        if 'Right Elbow' in joint_angles and joint_angles['Right Elbow'] > 160:
            feedback.append("Ensure your right elbow is fully extended at the bottom of the pull-up.")

        if 'Left Elbow' in joint_angles and joint_angles['Left Elbow'] > 160:
            feedback.append("Ensure your left elbow is fully extended at the bottom of the pull-up.")

        # Check if shoulders are properly engaged (angles between shoulders and torso)
        if 'Right Shoulder Flexion' in joint_angles and joint_angles['Right Shoulder Flexion'] < 45:
            feedback.append("Ensure your right shoulder is fully engaged at the top of the pull-up.")

        if 'Left Shoulder Flexion' in joint_angles and joint_angles['Left Shoulder Flexion'] < 45:
            feedback.append("Ensure your left shoulder is fully engaged at the top of the pull-up.")

        return feedback
