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

def autoplay_audio(file_path: str, placeholder):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay loop>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
    placeholder.markdown(md, unsafe_allow_html=True)

def play_audio_feedback(feedback):
    if 'audio_placeholder' not in st.session_state:
        st.session_state['audio_placeholder'] = st.empty()
    if 'last_played_audio' not in st.session_state:
        st.session_state['last_played_audio'] = None

    # If feedback is None or empty, stop any playing audio
    if not feedback:
        if st.session_state['last_played_audio'] is not None:
            st.session_state['audio_placeholder'].empty()
            st.session_state['last_played_audio'] = None
        return

    # If feedback has changed, update the audio
    if feedback != st.session_state['last_played_audio']:
        st.session_state['audio_placeholder'].empty()
        # Get or generate the audio file for the feedback
        feedback_audio_map = load_feedback_audio_map()
        audio_file = feedback_audio_map.get(feedback)

        if not audio_file or not os.path.exists(audio_file):
            # Generate the audio file using ElevenLabs API
            try:
                API_KEY = st.secrets["elevenlabs_api_key"]
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
                return
        else:
            # Audio file exists
            audio_filename = audio_file

        # Play the audio on loop
        autoplay_audio(audio_filename, st.session_state['audio_placeholder'])
        st.session_state['last_played_audio'] = feedback
    else:
        # Feedback is the same, do nothing (audio continues to loop)
        pass
