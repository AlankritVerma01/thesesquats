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
    
    #tts = ElevenLabsTextToSpeech(API_KEY)

    # Optionally change voice
    # tts.set_voice("9BWtsMINqrJLrRacOk9x")
    
    
    # Usage in streamlit
    # audio_stream = tts.synthesize_speech(text_input)
    # st.audio(audio_stream, format="audio/mp3")