def fetch_correct_vectors(exercise_name, collection):
    # Fetch correct exercise vectors from MongoDB
    correct_data = collection.find_one({"exercise": exercise_name})
    return correct_data["correct_vectors"]
