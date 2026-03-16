"""
audio_generator.py
Tries pyttsx3 first (offline), falls back to gTTS (online),
falls back to silence if both fail.
"""

import os
from config import CONFIG


def generate_audio(text: str, output_path: str) -> bool:
    """
    Generate audio narration for a slide.
    Tries pyttsx3 first, then gTTS, then silence.

    Returns True if audio was generated, False if silence used.
    """
    # Try 1 — pyttsx3 (works offline)
    if _try_pyttsx3(text, output_path):
        return True

    # Try 2 — gTTS (needs internet)
    if _try_gtts(text, output_path):
        return True

    # Try 3 — generate silence as fallback
    print(f"    Both TTS engines failed. Using silence.")
    _generate_silence(output_path)
    return False


def _try_pyttsx3(text: str, output_path: str) -> bool:
    """Try generating audio using pyttsx3 (offline TTS)"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', CONFIG["tts_rate"])
        engine.setProperty('volume', 1.0)
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        engine.stop()

        # Verify file was created and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
            print(f"    TTS: pyttsx3 success")
            return True
        return False

    except ImportError:
        print(f"    pyttsx3 not installed, trying gTTS...")
        return False
    except Exception as e:
        print(f"    pyttsx3 failed: {e}")
        return False


def _try_gtts(text: str, output_path: str) -> bool:
    """Try generating audio using gTTS (online TTS)"""
    try:
        from gtts import gTTS
        import tempfile

        # gTTS saves as mp3, convert to wav via temp file
        tts = gTTS(text=text, lang='en', slow=False)
        temp_mp3 = output_path.replace('.wav', '_temp.mp3')
        tts.save(temp_mp3)

        # Convert mp3 to wav using ffmpeg
        os.system(f'ffmpeg -y -i "{temp_mp3}" "{output_path}" -loglevel quiet')

        # Clean up temp file
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

        if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
            print(f"    TTS: gTTS success")
            return True
        return False

    except ImportError:
        print(f"    gTTS not installed, using silence...")
        return False
    except Exception as e:
        print(f"    gTTS failed: {e}")
        return False


def _generate_silence(output_path: str):
    """Generate a silent WAV file using FFmpeg as last fallback"""
    duration = CONFIG["slide_duration"]
    cmd = (
        f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono '
        f'-t {duration} "{output_path}" -loglevel quiet'
    )
    result = os.system(cmd)
    if result != 0:
        # If ffmpeg also fails, create a minimal WAV file manually
        _create_minimal_wav(output_path, duration)


def _create_minimal_wav(output_path: str, duration: float):
    """Create a minimal silent WAV file without ffmpeg"""
    import struct
    import math

    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = num_samples * block_align
    chunk_size = 36 + data_size

    with open(output_path, 'wb') as f:
        # WAV header
        f.write(b'RIFF')
        f.write(struct.pack('<I', chunk_size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))           # PCM format
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', bits_per_sample))
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        # Silent samples
        f.write(b'\x00\x00' * num_samples)