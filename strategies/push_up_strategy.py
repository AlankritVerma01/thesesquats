from strategies.exercise_strategy import ExerciseStrategy

class PushUpStrategy(ExerciseStrategy):
    def check_form(self, joint_angles, joint_distances):
        """
        Checks form during push-ups.
        """
        feedback = []
        buffers = {
            'elbow_angle': 10,  # degrees
            'spine_angle': 5    # degrees
        }

        # Elbow angle should be around 90 degrees at the bottom
        right_elbow_angle = joint_angles.get('Right Elbow')
        left_elbow_angle = joint_angles.get('Left Elbow')
        target_elbow_angle = 90

        if right_elbow_angle:
            if abs(right_elbow_angle - target_elbow_angle) > buffers['elbow_angle']:
                feedback.append("Try to bend your right elbow to about 90 degrees at the bottom of the push-up.")
        else:
            feedback.append("Right elbow not detected.")

        if left_elbow_angle:
            if abs(left_elbow_angle - target_elbow_angle) > buffers['elbow_angle']:
                feedback.append("Try to bend your left elbow to about 90 degrees at the bottom of the push-up.")
        else:
            feedback.append("Left elbow not detected.")

        # Spine angle should remain relatively straight
        spine_angle = joint_angles.get('Spine Angle')
        target_spine_angle = 180  # Straight line
        if spine_angle:
            if abs(spine_angle - target_spine_angle) > buffers['spine_angle']:
                feedback.append("Keep your back straight during the push-up.")
        else:
            feedback.append("Spine angle not detected.")

        return feedback
