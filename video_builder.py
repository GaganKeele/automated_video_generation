"""
video_builder.py
Uses MoviePy to combine slide images + audio into final .mp4 video
"""

import os
from config import CONFIG


def build_video(slide_paths: list, audio_paths: list,
                output_path: str, slide_duration: int = 5):
    """
    Build final MP4 video from slide images and audio files.

    Args:
        slide_paths:    List of paths to slide PNG images
        audio_paths:    List of paths to audio WAV files (can be None)
        output_path:    Where to save the final MP4
        slide_duration: Seconds per slide if no audio
    """
    try:
        from moviepy.editor import (
            ImageClip, AudioFileClip, CompositeAudioClip,
            concatenate_videoclips, concatenate_audioclips
        )

        clips = []

        for i, (img_path, audio_path) in enumerate(
                zip(slide_paths, audio_paths)):

            print(f"  Building clip {i+1}/{len(slide_paths)}...")

            # Determine duration from audio or use default
            if audio_path and os.path.exists(audio_path):
                try:
                    audio_clip = AudioFileClip(audio_path)
                    duration = audio_clip.duration + CONFIG["silence_duration"]
                    audio_clip.close()
                except Exception:
                    duration = slide_duration
            else:
                duration = slide_duration

            # Create image clip
            img_clip = ImageClip(img_path).set_duration(duration)

            # Attach audio if available
            if audio_path and os.path.exists(audio_path):
                try:
                    audio_clip = AudioFileClip(audio_path)
                    img_clip = img_clip.set_audio(audio_clip)
                except Exception as e:
                    print(f"    Could not attach audio: {e}")

            clips.append(img_clip)

        if not clips:
            print("ERROR: No clips were created!")
            return

        # Concatenate all clips
        print("\n  Concatenating all clips...")
        final_video = concatenate_videoclips(clips, method="compose")

        # Write final video
        print(f"  Encoding final video → {output_path}")
        final_video.write_videofile(
            output_path,
            fps=CONFIG["fps"],
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="output/temp_audio.m4a",
            remove_temp=True,
            logger=None
        )

        # Close all clips to free memory
        final_video.close()
        for clip in clips:
            clip.close()

        print(f"\n  Video saved successfully: {output_path}")

    except ImportError:
        print("\nERROR: MoviePy not installed!")
        print("Run: pip install moviepy")
    except Exception as e:
        print(f"\nERROR building video: {e}")
        raise