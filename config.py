"""
config.py - All configurable parameters in one place
Change these values to customize your video output
"""

CONFIG = {
    # Input / Output
    "input_file":     "input/script.txt",
    "output_file":    "output/explainer_video.mp4",

    # Video settings
    "width":          1280,       # Resolution width (configurable)
    "height":         720,        # Resolution height
    "fps":            24,         # Frames per second
    "slide_duration": 5,          # Seconds per slide (configurable)

    # Font settings
    "font_size":      42,         # Main text font size (configurable)
    "title_font_size": 52,        # Title font size
    "font_color":     (255, 255, 255),   # White text
    "bg_color":       (15, 23, 42),      # Dark navy background

    # Slide appearance
    "padding":        80,         # Padding around text in pixels
    "line_spacing":   1.4,        # Space between lines

    # Audio settings
    "tts_rate":       150,        # Speech rate (words per minute, configurable)
    "silence_duration": 0.5,      # Silence between slides (seconds)
}