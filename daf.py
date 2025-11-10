# daf.py
import sounddevice as sd
import numpy as np
from collections import deque

SAMPLE_RATE = 16000
CHANNELS = 1
DELAY_MS = 120      # Adjust: 50–200 ms
FRAME_MS = 20       # Frame size (20 ms per buffer)

frame_size = int(SAMPLE_RATE * FRAME_MS / 1000)
delay_frames = int(DELAY_MS / FRAME_MS)
buffer = deque(maxlen=(delay_frames + 5))

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    buffer.append(indata[:, 0].copy())
    if len(buffer) <= delay_frames:
        outdata[:] = np.zeros((frames, 1), dtype=np.float32)
    else:
        outdata[:, 0] = buffer[0]

def run_daf():
    print(f"DAF active — {DELAY_MS} ms delay. Speak into the mic. Ctrl+C to stop.")
    with sd.Stream(samplerate=SAMPLE_RATE,
                   blocksize=frame_size,
                   dtype='float32',
                   channels=CHANNELS,
                   callback=callback):
        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("\nStopped DAF.")
