def check_exercise_form(angles):
    """Checks if the exercise form is correct based on the angles."""
    violations = []

    # Rule 1: Check if right elbow angle is within a specific range for overhead press
    if 'Right Elbow' in angles and (angles['Right Elbow'] < 80 or angles['Right Elbow'] > 170):
        violations.append("Right Elbow should be between 80° and 170°.")

    # Rule 2: Check for shoulder alignment
    if 'Shoulder Flexion' in angles and (angles['Shoulder Flexion'] < 60 or angles['Shoulder Flexion'] > 180):
        violations.append("Shoulder flexion should be between 60° and 180°.")

    # Add more rules for other joints (knees, hips, spine, etc.)

    return violations if violations else None
