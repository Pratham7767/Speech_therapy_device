# Speech_therapy_device
A Python-based Speech Therapy Assistant using Whisper ASR, Delayed Auditory Feedback (DAF), and Frequency-Shifted Feedback (FSF) to improve speech fluency and clarity. Designed for Raspberry Pi or Ubuntu, it provides real-time auditory correction and transcription-based progress tracking.


# 🗣️ Speech Therapy Assistant

## Overview  
This project implements a **Speech Therapy Assistant** that helps users improve speech fluency and articulation through **real-time auditory feedback** and **automatic speech recognition**.

It integrates:
- 🎧 **DAF (Delayed Auditory Feedback)** — helps control speech pacing.  
- 🎵 **FSF (Frequency-Shifted Feedback)** — alters pitch to improve clarity and reduce stuttering.  
- 🧠 **Whisper ASR** — transcribes speech to compare it with a reference sentence.

This version records for a **fixed duration of 10 seconds** and provides corrective feedback based on the difference between the spoken and reference sentences.

---

## 🧩 Features
- 🎤 Real-time recording and playback  
- 🧠 Whisper-powered speech transcription  
- 🔁 DAF and FSF feedback modes for correction  
- ⚙️ Adjustable delay (ms) and pitch shift (semitones)  
- 💻 Works seamlessly on **Ubuntu** and **Raspberry Pi 4**

---

## ⚙️ Hardware Requirements
- Raspberry Pi 4 (or any Linux PC)
- USB headset (with mic and speaker)
- Internet connection (for model installation)

---

## 🧠 Software Requirements

Make sure Python 3.10+ is installed.  
Then install dependencies:

```bash
sudo apt update
sudo apt install python3-pip portaudio19-dev ffmpeg soundstretch -y
pip install numpy sounddevice soundfile openai-whisper

for more info visit requirements.txt
