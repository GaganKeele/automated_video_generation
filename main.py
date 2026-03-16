import os
import sys
from config import CONFIG
from text_processor import read_and_split_text
from slide_generator import generate_slide_image
from audio_generator import generate_audio
from video_builder import build_video

def main():
    print("=" * 55)
    print("  Automated Explainer Video Generator")
    print("  Assessment 2 - AI Intern")
    print("=" * 55)

    # ── STEP 1: Read Input ──────────────────────────────────
    input_file = CONFIG["input_file"]

    if not os.path.exists(input_file):
        print(f"\nERROR: Input file '{input_file}' not found!")
        print("Please create input/script.txt with your text.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read().strip()

    if not raw_text:
        print("\nERROR: Input file is empty!")
        sys.exit(1)

    print(f"\nLoaded input from: {input_file}")

    # ── STEP 2: Split Text Into Slides ──────────────────────
    print("\nSplitting text into slides...")
    slides = read_and_split_text(raw_text)
    print(f"  Created {len(slides)} slides")

    # ── STEP 3: Create Output Folders ──────────────────────
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/slides", exist_ok=True)
    os.makedirs("output/audio", exist_ok=True)

    # ── STEP 4: Generate Slide Images + Audio ──────────────
    slide_paths = []
    audio_paths = []

    for i, slide_text in enumerate(slides):
        print(f"\nProcessing slide {i+1}/{len(slides)}...")

        # Generate slide image
        img_path = f"output/slides/slide_{i+1:03d}.png"
        generate_slide_image(
            text=slide_text,
            slide_number=i+1,
            total_slides=len(slides),
            output_path=img_path
        )
        slide_paths.append(img_path)
        print(f"  Slide image saved: {img_path}")

        # Generate audio narration
        audio_path = f"output/audio/audio_{i+1:03d}.wav"
        success = generate_audio(slide_text, audio_path)
        audio_paths.append(audio_path if success else None)
        if success:
            print(f"  Audio saved: {audio_path}")
        else:
            print(f"  Audio failed - will use silence")

    # ── STEP 5: Build Final Video ───────────────────────────
    print("\nBuilding final video...")
    output_video = CONFIG["output_file"]

    build_video(
        slide_paths=slide_paths,
        audio_paths=audio_paths,
        output_path=output_video,
        slide_duration=CONFIG["slide_duration"]
    )

    # ── STEP 6: Done ────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  VIDEO GENERATION COMPLETE")
    print("=" * 55)
    print(f"  Input file    : {input_file}")
    print(f"  Total slides  : {len(slides)}")
    print(f"  Output video  : {output_video}")
    print(f"  Resolution    : {CONFIG['width']}x{CONFIG['height']}")
    print(f"  Slide duration: {CONFIG['slide_duration']}s per slide")
    print("=" * 55)

if __name__ == "__main__":
    main()