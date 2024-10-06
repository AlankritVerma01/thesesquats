import requests
import json
import os
import io

class ElevenLabsTextToSpeech:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice ID (Rachel)

    def set_voice(self, voice_id):
        self.voice_id = voice_id

    def get_voices(self):
        endpoint = f"{self.base_url}/voices"
        response = requests.get(endpoint, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get voices: {response.text}")

    def synthesize_speech(self, text, model_id="eleven_monolingual_v1"):
        endpoint = f"{self.base_url}/text-to-speech/{self.voice_id}/stream"
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(endpoint, json=data, headers=self.headers)
        
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            raise Exception(f"Speech synthesis failed: {response.text}")

# Example usage
if __name__ == "__main__":
    API_KEY = os.getenv('API_KEY')
    
    tts = ElevenLabsTextToSpeech(API_KEY)

    sentences = [
        "Keep your spine straight, avoid bending forward or backward during the curl.",
        "Avoid swinging your left shoulder during the curl.",
        "Avoid swinging your right shoulder during the curl.",
        "Ensure proper shoulder engagement on the right side.",
        "Ensure proper shoulder engagement on the left side.",
        "Avoid pushing your right knee too far over your toes.",
        "Avoid pushing your left knee too far over your toes.",
        "Keep your upper body straight during the lunge.",
        "Ensure your right elbow is fully extended at the bottom of the pull-up.",
        "Ensure your left elbow is fully extended at the bottom of the pull-up.",
        "Ensure your right shoulder is fully engaged at the top of the pull-up.",
        "Ensure your left shoulder is fully engaged at the top of the pull-up.",
        "Keep your back straight during the push-up.",
        "Keep your back straight during the squat.",
        "Ensure your left hip bends to about 90 degrees during the squat.",
        "Ensure your right hip bends to about 90 degrees during the squat."
    ]

    output_dir = "../voice/"
    os.makedirs(output_dir, exist_ok=True)

    for i, sentence in enumerate(sentences):
        try:
            audio_stream = tts.synthesize_speech(sentence)
            output_file = os.path.join(output_dir, f"sentence_{i+1}.mp3")
            
            with open(output_file, "wb") as f:
                f.write(audio_stream.getvalue())
            
            print(f"Generated audio for sentence {i+1} and saved to {output_file}")
        except Exception as e:

            print(f"Error generating audio for sentence {i+1}: {str(e)}")

    print("Audio generation complete.") 
