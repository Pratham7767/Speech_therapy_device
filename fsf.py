# fsf.py
import subprocess
import os

def shift_pitch(input_wav, output_wav, semitones):
    """
    Shifts pitch by ±semitones using soundstretch CLI.
    Example: shift_pitch("input.wav", "output.wav", -3)
    """
    if not os.path.exists(input_wav):
        raise FileNotFoundError(f"Input file not found: {input_wav}")
    cmd = ["soundstretch", input_wav, output_wav, f"-pitch={semitones}"]
    subprocess.run(cmd, check=True)
    print(f"Saved pitch-shifted file to {output_wav}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Frequency-shift an audio file")
    parser.add_argument("input", help="Input WAV file")
    parser.add_argument("output", help="Output WAV file")
    parser.add_argument("semitones", type=float, help="Pitch shift in semitones (+/-)")
    args = parser.parse_args()

    shift_pitch(args.input, args.output, args.semitones)
