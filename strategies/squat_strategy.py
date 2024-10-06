from strategies.exercise_strategy import ExerciseStrategy

class SquatStrategy(ExerciseStrategy):
    def check_form(self, joint_angles, joint_distances):
        """
        Checks form during squats.
        """
        feedback = []
        buffers = {
            'knee_angle': 10,   # degrees
            'hip_angle': 10,    # degrees
            'spine_angle': 5    # degrees
        }

        # Knee angle should be around 90 degrees at the bottom
        right_knee_angle = joint_angles.get('Right Knee')
        left_knee_angle = joint_angles.get('Left Knee')
        target_knee_angle = 90

        if right_knee_angle:
            if abs(right_knee_angle - target_knee_angle) > buffers['knee_angle']:
                feedback.append("Try to bend your right knee to about 90 degrees when squatting.")
        else:
            feedback.append("Right knee not detected.")

        if left_knee_angle:
            if abs(left_knee_angle - target_knee_angle) > buffers['knee_angle']:
                feedback.append("Try to bend your left knee to about 90 degrees when squatting.")
        else:
            feedback.append("Left knee not detected.")

        # Hip angle should also be around 90 degrees
        right_hip_angle = joint_angles.get('Right Hip')
        left_hip_angle = joint_angles.get('Left Hip')
        target_hip_angle = 90

        if right_hip_angle:
            if abs(right_hip_angle - target_hip_angle) > buffers['hip_angle']:
                feedback.append("Ensure your right hip bends to about 90 degrees during the squat.")
        else:
            feedback.append("Right hip not detected.")

        if left_hip_angle:
            if abs(left_hip_angle - target_hip_angle) > buffers['hip_angle']:
                feedback.append("Ensure your left hip bends to about 90 degrees during the squat.")
        else:
            feedback.append("Left hip not detected.")

        # Spine should remain relatively straight
        spine_angle = joint_angles.get('Spine Angle')
        target_spine_angle = 180  # Straight line
        if spine_angle:
            if abs(spine_angle - target_spine_angle) > buffers['spine_angle']:
                feedback.append("Keep your back straight during the squat.")
        else:
            feedback.append("Spine angle not detected.")

        return feedback
