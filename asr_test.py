"""
Speech Therapy Assistant (Simplified)

This simplified version removes noise calibration and automatic end-of-speech detection.
It records for a fixed duration (default 10 seconds) and supports DAF and FSF feedback modes.
"""

import os
import wave
import subprocess
from difflib import SequenceMatcher

import numpy as np
import sounddevice as sd
import soundfile as sf
import whisper

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 10  # Fixed duration of recording
DEFAULT_DAF_MS = 120
DEFAULT_FSF_SEMITONES = -3.0
WHISPER_MODEL_NAME = "small"

# -------------------------------------------------------------
# Initialize Whisper model
# -------------------------------------------------------------
print("Loading Whisper model... this may take a moment")
model = whisper.load_model(WHISPER_MODEL_NAME)
print("Whisper model loaded")

# -------------------------------------------------------------
# Audio utility functions
# -------------------------------------------------------------
def record_fixed(filename, seconds=RECORD_SECONDS):
    """Record fixed-duration audio and save to a WAV file."""
    print(f"Recording for {seconds} seconds... Speak now!")
    data = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.tobytes())
    print(f"Saved {filename}")


def play_audio(filename):
    """Play a WAV file using sounddevice."""
    if not os.path.exists(filename):
        print("Error: file not found ->", filename)
        return
    data, sr = sf.read(filename, dtype='float32')
    sd.play(data, sr)
    sd.wait()


def shift_pitch_cli(input_wav, output_wav, semitones):
    """Use SoundTouch's soundstretch CLI to shift pitch by given semitones."""
    if not os.path.exists(input_wav):
        raise FileNotFoundError(f"Input file not found: {input_wav}")
    cmd = ["soundstretch", input_wav, output_wav, f"-pitch={semitones}"]
    subprocess.run(cmd, check=True)
    print(f"Pitch-shifted {input_wav} -> {output_wav} ({semitones} semitones)")


def transcribe_whisper(audio_path, language='en'):
    """Transcribe a WAV file using Whisper."""
    print("Transcribing with Whisper...")
    res = model.transcribe(audio_path, language=language)
    text = res.get('text', '').strip()
    return text


def compare_texts(reference, spoken):
    """Compare reference and spoken text word by word."""
    ref_words = reference.lower().split()
    spoken_words = spoken.lower().split()
    sm = SequenceMatcher(None, ref_words, spoken_words)
    diffs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            diffs.append({
                'type': tag,
                'expected': ' '.join(ref_words[i1:i2]),
                'spoken': ' '.join(spoken_words[j1:j2])
            })
    return diffs

# -------------------------------------------------------------
# DAF Recording
# -------------------------------------------------------------
class DAFRecorder:
    def __init__(self, delay_ms=DEFAULT_DAF_MS, duration=RECORD_SECONDS):
        self.delay_ms = delay_ms
        self.duration = duration

    def record(self, out_filename):
        """Record audio with delayed playback (DAF)."""
        delay_samples = int((self.delay_ms / 1000.0) * SAMPLE_RATE)
        print(f"DAF active ({self.delay_ms} ms delay). Speak now!")
        total_samples = int(self.duration * SAMPLE_RATE)
        buffer = np.zeros((delay_samples,), dtype='int16')
        recorded = np.zeros((total_samples,), dtype='int16')
        with sd.Stream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
            for i in range(total_samples):
                in_frame, _ = stream.read(1)
                recorded[i] = in_frame[0][0]
                if i >= delay_samples:
                    stream.write(np.array([[recorded[i - delay_samples]]], dtype='int16'))
                else:
                    stream.write(np.array([[0]], dtype='int16'))
        with wave.open(out_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(recorded.tobytes())
        print(f"Saved DAF recording: {out_filename}")

# -------------------------------------------------------------
# Main therapy loop
# -------------------------------------------------------------
def therapy_loop():
    print("Speech Therapy Assistant — Whisper + DAF + FSF (Fixed Duration Mode)")
    reference = input("Enter reference sentence → ").strip()

    daf_default = DEFAULT_DAF_MS
    fsf_default = DEFAULT_FSF_SEMITONES

    attempt = 1
    while True:
        print(f"--- ROUND #{attempt} ---")
        base_file = f"attempt_{attempt}_orig.wav"
        record_fixed(base_file)
        play_audio(base_file)

        spoken_text = transcribe_whisper(base_file)
        print(f"Transcribed: {spoken_text}")

        diffs = compare_texts(reference, spoken_text)
        if not diffs:
            print("Perfect match — well done!")
            break
        else:
            print("Differences detected:")
            for d in diffs:
                print(f"  Expected '{d['expected']}' but heard '{d['spoken']}'")

        choice = input("Choose feedback mode (daf / fsf / skip): ").strip().lower()
        if choice == 'daf':
            daf_rec = DAFRecorder(delay_ms=daf_default)
            daf_file = f"attempt_{attempt}_daf.wav"
            daf_rec.record(daf_file)
            spoken_text = transcribe_whisper(daf_file)
        elif choice == 'fsf':
            shifted_name = f"attempt_{attempt}_shifted.wav"
            shift_pitch_cli(base_file, shifted_name, fsf_default)
            play_audio(shifted_name)
            record_fixed(f"attempt_{attempt}_fsf.wav")
        else:
            print("Skipping feedback.")

        again = input("Try again? (y/n): ").strip().lower()
        if again != 'y':
            break
        attempt += 1

# -------------------------------------------------------------
# Run
# -------------------------------------------------------------
if __name__ == '__main__':
    therapy_loop()
