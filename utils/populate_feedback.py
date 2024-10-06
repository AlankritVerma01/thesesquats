# utils/populate_feedback_audio_map.py

import os
import json
from voice_utils import sanitize_filename, load_feedback_audio_map, save_feedback_audio_map

# List of feedback messages and their corresponding audio file names
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

def main():
    feedback_audio_map = load_feedback_audio_map()
    audio_dir = 'voice'

    for i, sentence in enumerate(sentences):
        sanitized_feedback = sanitize_filename(sentence)
        audio_filename = os.path.join(audio_dir, f"sentence_{i+1}.mp3")

        # Check if the audio file exists
        if os.path.exists(audio_filename):
            # Update the mapping
            feedback_audio_map[sentence] = audio_filename
            print(f"Mapped '{sentence}' to '{audio_filename}'")
        else:
            print(f"Audio file '{audio_filename}' not found for sentence '{sentence}'")

    # Save the updated mapping
    save_feedback_audio_map(feedback_audio_map)
    print("Feedback audio mapping updated.")

if __name__ == "__main__":
    main()
