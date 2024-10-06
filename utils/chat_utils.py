import requests

def get_ai_recommendation(user_input):
    """
    Send user input to an AI chat endpoint and get a workout recommendation.
    """
    endpoint = "https://ancient-bush-78c5.deezsquats.workers.dev/"  # Replace with the actual endpoint
    response = requests.post(endpoint, json={"userPrompt": "I feel like doing some arms today what should I do?"})
    
    # Return the AI response, which includes workout plan suggestions
    return response.json()  # Expected response to contain {"ai_reply": "...", "recommended_exercises": [...]}
