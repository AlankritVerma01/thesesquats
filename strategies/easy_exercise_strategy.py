from strategies.exercise_strategy import ExerciseStrategy

class EasyExerciseStrategy(ExerciseStrategy):
    def check_form(self, joint_angles, joint_distances):
        """
        Simple check for arm angles below 90 degrees.
        joint_angles: dictionary with joint names as keys and their calculated angles as values
        joint_distances: dictionary with joint names as keys and their distances as values
        """
        feedback = []
        
        # Check if any arm angle is below 90 degrees
        if joint_angles.get('Right Elbow', 180) < 90:
            feedback.append("Check your right arm, angle is less than 90 degrees.")
        
        if joint_angles.get('Left Elbow', 180) < 90:
            feedback.append("Check your left arm, angle is less than 90 degrees.")
        
        return feedback
