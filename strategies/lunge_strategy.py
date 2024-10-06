from strategies.exercise_strategy import ExerciseStrategy

class LungeStrategy(ExerciseStrategy):
    def check_form(self, joint_angles, joint_distances):
        """
        Checks form during lunges.
        """
        feedback = []
        buffers = {
            'knee_angle': 10,     # degrees
            'hip_angle': 10,      # degrees
            'knee_over_toes': 5   # degrees
        }

        # Front knee should be around 90 degrees
        right_knee_angle = joint_angles.get('Right Knee')
        left_knee_angle = joint_angles.get('Left Knee')
        target_knee_angle = 90

        if right_knee_angle:
            if abs(right_knee_angle - target_knee_angle) > buffers['knee_angle']:
                feedback.append("Bend your right knee to about 90 degrees in the lunge.")
        else:
            feedback.append("Right knee not detected.")

        if left_knee_angle:
            if abs(left_knee_angle - target_knee_angle) > buffers['knee_angle']:
                feedback.append("Bend your left knee to about 90 degrees in the lunge.")
        else:
            feedback.append("Left knee not detected.")

        # Check if knee is not going too far over the toes
        # This requires calculating the forward angle of the shin, which may not be directly available
        # For simplicity, let's assume we want to keep the knee angle greater than 80 degrees

        if right_knee_angle and right_knee_angle < (80 + buffers['knee_over_toes']):
            feedback.append("Avoid pushing your right knee too far over your toes.")
        if left_knee_angle and left_knee_angle < (80 + buffers['knee_over_toes']):
            feedback.append("Avoid pushing your left knee too far over your toes.")

        # Hip angle should allow for an upright torso
        spine_angle = joint_angles.get('Spine Angle')
        target_spine_angle = 180  # Upright position

        if spine_angle:
            if abs(spine_angle - target_spine_angle) > buffers['hip_angle']:
                feedback.append("Keep your upper body straight during the lunge.")
        else:
            feedback.append("Spine angle not detected.")

        return feedback
