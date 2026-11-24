
import os
import subprocess
import tempfile
import wave

import sounddevice as sd
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
RECORD_SECONDS = 6

# Load the speech recognition model once.
whisper_model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)


def listen():
    """Record microphone audio and convert it into text."""

    print("\n🎤 Listening for 6 seconds...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    # Whisper accepts WAV audio files.
    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temporary_file:
        audio_path = temporary_file.name

    try:
        with wave.open(audio_path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(audio.tobytes())

        segments, info = whisper_model.transcribe(
            audio_path,
            beam_size=3,
            language="en",
            vad_filter=True
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        return text

    finally:
        os.remove(audio_path)


def speak(text):
    """Speak a response using macOS text-to-speech."""

    subprocess.run(
        ["say", "-v", "Daniel", text],
        check=False
    )
