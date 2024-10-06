# overhead_press_strategy.py

from strategies.exercise_strategy import ExerciseStrategy

class OverheadPressStrategy(ExerciseStrategy):
    def check_form(self, joint_angles, joint_distances):
        """
        Checks form during the overhead press exercise.
        """
        feedback = []
        buffers = {
            'elbow_angle': 20,       # degrees buffer for elbow extension
            'shoulder_angle': 20,    # degrees buffer for shoulder flexion
            'spine_angle': 30,        # degrees buffer for spine alignment
            'wrist_alignment': 90,   # degrees buffer for wrist alignment
        }

        # Check Elbow Extension at the Top
        right_elbow_angle = joint_angles.get('Right Elbow')
        left_elbow_angle = joint_angles.get('Left Elbow')
        target_elbow_angle_top = 180  # Fully extended

        if right_elbow_angle:
            if abs(right_elbow_angle - target_elbow_angle_top) > buffers['elbow_angle']:
                feedback.append("Fully extend your right elbow at the top of the press.")
        else:
            feedback.append("Right elbow not detected.")

        if left_elbow_angle:
            if abs(left_elbow_angle - target_elbow_angle_top) > buffers['elbow_angle']:
                feedback.append("Fully extend your left elbow at the top of the press.")
        else:
            feedback.append("Left elbow not detected.")

        # Check Shoulder Flexion Angle
        right_shoulder_flexion = joint_angles.get('Right Shoulder Flexion')
        left_shoulder_flexion = joint_angles.get('Left Shoulder Flexion')
        target_shoulder_angle_top = 180  # Arms overhead

        if right_shoulder_flexion:
            if abs(right_shoulder_flexion - target_shoulder_angle_top) > buffers['shoulder_angle']:
                feedback.append("Lift your right arm fully overhead.")
        else:
            feedback.append("Right shoulder not detected.")

        if left_shoulder_flexion:
            if abs(left_shoulder_flexion - target_shoulder_angle_top) > buffers['shoulder_angle']:
                feedback.append("Lift your left arm fully overhead.")
        else:
            feedback.append("Left shoulder not detected.")

        # Check Spine Alignment
        spine_angle = joint_angles.get('Spine Angle')
        target_spine_angle = 180  # Neutral spine

        if spine_angle:
            if abs(spine_angle - target_spine_angle) > buffers['spine_angle']:
                feedback.append("Keep your back straight and avoid arching during the press.")
        else:
            feedback.append("Spine angle not detected.")

        # Optional: Check Wrist Alignment (if you have wrist keypoints)
        # Since wrist alignment can be tricky without 3D data, you might skip this or implement a basic check if possible.

        return feedback
