# utils/voice_utils.py

import os
import json
import io
import requests
import streamlit as st
import base64
# Path to the mapping file
MAPPING_FILE = 'feedback_audio_map.json'
# Directory to store audio files
AUDIO_DIR = 'voice'

class ElevenLabsTextToSpeech:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice ID

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

def load_feedback_audio_map():
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, 'r') as f:
            feedback_audio_map = json.load(f)
    else:
        feedback_audio_map = {}
    return feedback_audio_map

def save_feedback_audio_map(feedback_audio_map):
    with open(MAPPING_FILE, 'w') as f:
        json.dump(feedback_audio_map, f)

def sanitize_filename(text):
    sanitized = text.replace(" ", "_").replace("/", "_").replace("\\", "_")
    sanitized = "".join(c for c in sanitized if c.isalnum() or c in ('_',))
    return sanitized[:50]  # Limit filename length

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
def play_audio_feedback(feedback):
    if 'audio_placeholder' not in st.session_state:
        st.session_state['audio_placeholder'] = st.empty()
    if 'last_played_audio' not in st.session_state:
        st.session_state['last_played_audio'] = None

    feedback_audio_map = load_feedback_audio_map()

    # Check if the feedback message is already in the mapping
    audio_file = feedback_audio_map.get(feedback)

    if not audio_file or not os.path.exists(audio_file):
        # Generate the audio file using ElevenLabs API
        try:
            # Initialize the TTS API
            #API_KEY = os.getenv('ELEVENLABS_API_KEY')  # Ensure your API key is set
            API_KEY = "sk_f658e8338c02622e5228bea687a989da86ebcf04f535038a"
            if not API_KEY:
                st.write("Error: ElevenLabs API key is not set.")
                return
            tts = ElevenLabsTextToSpeech(API_KEY)
            # Generate the audio
            audio_stream = tts.synthesize_speech(feedback)
            # Save the audio file
            sanitized_feedback = sanitize_filename(feedback)
            audio_filename = os.path.join(AUDIO_DIR, f"{sanitized_feedback}.mp3")
            os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
            with open(audio_filename, 'wb') as f:
                f.write(audio_stream.getvalue())
            # Update the mapping
            feedback_audio_map[feedback] = audio_filename
            save_feedback_audio_map(feedback_audio_map)
        except Exception as e:
            st.write(f"Error generating audio for feedback: {feedback}. Error: {str(e)}")
            return  # Exit the function if there's an error
    else:
        # Audio file exists, proceed to play
        audio_filename = audio_file

    # Play the audio if it's different from the last played feedback
    if feedback != st.session_state['last_played_audio']:
        st.session_state['audio_placeholder'].empty()  # Clear previous audio
        # st.session_state['audio_placeholder'].audio(audio_filename, format='audio/mp3')
        autoplay_audio(audio_filename)
        st.session_state['last_played_audio'] = feedback
