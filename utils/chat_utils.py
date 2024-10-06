import requests

def get_ai_recommendation(user_input):
    """
    Send user input to an AI chat endpoint and get a workout recommendation.
    """
    endpoint = "https://square-sea-c796.nelodukasobe.workers.dev/"
    response = requests.post(endpoint, json={"userPrompt": user_input})
    
    # Return the AI response, which includes workout plan suggestions
    return response.json()  # Expected response to contain {"ai_reply": "...", "recommended_exercises": [...]}
