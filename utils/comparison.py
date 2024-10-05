def compare_vectors(user_vectors, correct_vectors, threshold=0.05):
    errors = []
    for user, correct in zip(user_vectors, correct_vectors):
        if abs(user['vector'][0] - correct['vector'][0]) > threshold or \
           abs(user['vector'][1] - correct['vector'][1]) > threshold:
            errors.append(f"Incorrect form at {user['keypoint']}")
    return errors
