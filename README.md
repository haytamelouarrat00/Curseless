# Curseless

# Audio Profanity Censor

A robust deep learning-based system for automated detection and censorship of profanity in audio content. This solution
leverages OpenAI's Whisper model for precise speech recognition and implements sophisticated audio processing techniques
to seamlessly replace inappropriate content with customizable beep sounds.

## Features

The system provides comprehensive audio content moderation capabilities:

- State-of-the-art speech recognition using OpenAI's Whisper model
- Precise word-level timestamp detection for accurate censoring
- Automated profanity detection with adjustable sensitivity
- Seamless audio replacement with configurable beep sounds
- Smooth audio transitions with fade effects
- Detailed reporting of detected instances
- Support for multiple audio formats
- GPU acceleration for enhanced performance

## Prerequisites

This project requires Python 3.8 or later and the following dependencies:

- PyTorch
- OpenAI Whisper
- PyDub
- better-profanity
- FFmpeg (required for audio processing)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/audio-profanity-censor.git
cd audio-profanity-censor
```

2. Install FFmpeg:
	- Windows: Download from https://github.com/BtbN/FFmpeg-Builds/releases
	- Linux: `sudo apt-get install ffmpeg`
	- macOS: `brew install ffmpeg`

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Implementation

```python
from audio_censor import AudioCensor

# Initialize the censor with a beep sound
censor = AudioCensor("assets/beep.mp3")

# Process an audio file
censor.process_audio("input.mp3", "censored_output.mp3")
```

### Advanced Configuration

```python
# Initialize with custom settings
censor = AudioCensor(
    beep_sound_path="assets/custom_beep.mp3",
    model_size="base"  # Options: tiny, base, small, medium, large
)

# Process audio with detailed reporting
censored_segments = censor.process_audio(
    input_path="input.mp3",
    output_path="censored_output.mp3"
)

# Print censorship report
print(f"Found {len(censored_segments)} instances of profanity:")
for segment in censored_segments:
    print(f"- '{segment['word']}' at {segment['start']:.2f}s - {segment['end']:.2f}s")
```

## Project Structure

```
audio-profanity-censor/
├── src/
│   ├── main.py              # Main application entry point
│   └── audio_censor.py      # Core censorship implementation
├── assets/
│   └── beep.mp3            # Default beep sound
├── tests/
│   └── test_censor.py      # Unit tests
├── examples/
│   └── example_usage.py    # Usage examples
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Performance Considerations

The system's performance depends on several factors:

- Audio file length and quality
- Selected Whisper model size
- Hardware capabilities (GPU availability)
- Input audio format and complexity

For optimal performance, consider:

- Using GPU acceleration when available
- Selecting appropriate Whisper model size based on accuracy needs
- Processing audio files in standard formats (MP3, WAV)
- Ensuring adequate system resources for processing

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper model
- PyDub developers for audio processing capabilities
- better-profanity library contributors

## Contact

For questions and support, please open an issue in the GitHub repository or contact the maintainers directly.
