from strategies.exercise_strategy import ExerciseStrategy

class BicepCurlStrategy(ExerciseStrategy):
    def check_form(self, joint_angles, joint_distances):
        """
        Checks form during bicep curls.
        """
        feedback = []
        buffers = {
            'elbow_angle': 20,   # degrees
            'shoulder_angle': 40, # degrees
            'spine_angle': 10 # degrees
        }

        # Elbow angle should move from near 180 degrees (arm extended) to about 30 degrees (arm curled)
        right_elbow_angle = joint_angles.get('Right Elbow')
        left_elbow_angle = joint_angles.get('Left Elbow')

        if right_elbow_angle:
            if right_elbow_angle > (180 - buffers['elbow_angle']):
                feedback.append("Fully extend your right arm at the bottom of the curl.")
            elif right_elbow_angle < (30 + buffers['elbow_angle']):
                feedback.append("Curl your right arm up to about 30 degrees.")
        else:
            pass
            # feedback.append("Right elbow not detected.")

        if left_elbow_angle:
            if left_elbow_angle > (180 - buffers['elbow_angle']):
                feedback.append("Fully extend your left arm at the bottom of the curl.")
            elif left_elbow_angle < (30 + buffers['elbow_angle']):
                feedback.append("Curl your left arm up to about 30 degrees.")
        else:
            pass
            # feedback.append("Left elbow not detected.")

        # Shoulder should remain relatively stable
        right_shoulder_angle = joint_angles.get('Right Shoulder Flexion')
        left_shoulder_angle = joint_angles.get('Left Shoulder Flexion')
        target_shoulder_angle = 0  # Minimal movement

        if right_shoulder_angle:
            if abs(right_shoulder_angle - target_shoulder_angle) > buffers['shoulder_angle']:
                feedback.append("Avoid swinging your right shoulder during the curl.")
        else:
            pass
            # feedback.append("Right shoulder not detected.")

        if left_shoulder_angle:
            if abs(left_shoulder_angle - target_shoulder_angle) > buffers['shoulder_angle']:
                feedback.append("Avoid swinging your left shoulder during the curl.")
        else:
            pass
            # feedback.append("Left shoulder not detected.")

        # Spine should remain straight
        spine_angle = joint_angles.get('Spine Angle')
        target_spine_angle = 0  # Neutral spine position

        if spine_angle:
            if abs(spine_angle - target_spine_angle) > buffers['spine_angle']:
                feedback.append("Keep your spine straight, avoid bending forward or backward during the curl.")
        else:
            pass
            # feedback.append("Spine angle not detected.")

        return feedback