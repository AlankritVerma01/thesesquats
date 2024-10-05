import cv2
import matplotlib.pyplot as plt
import streamlit as st

def save_video(uploaded_video):
    """Saves the uploaded video to a temporary file."""
    video_path = f"temp_video.{uploaded_video.name.split('.')[-1]}"
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
    return video_path

def plot_joint_angles(joint_angles, joint_name):
    """Plots the joint angles for a specific joint over time."""
    plt.figure()
    plt.plot(joint_angles, label=f"{joint_name} Angle")
    plt.xlabel("Frame Number")
    plt.ylabel("Angle (degrees)")
    plt.title(f"{joint_name} Angle Over Time")
    plt.legend()
    st.pyplot(plt)
