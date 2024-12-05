import whisper
import torch
from pydub import AudioSegment
from typing import Dict, List, Tuple
from better_profanity import profanity


class AudioContentModerator:
    def __init__(self, replacement_sound_path: str, censorship_threshold: float = 0.8, model_size: str = "base"):
        """
        Initialize the content moderation system with Whisper model.

        Args:
            replacement_sound_path: Path to the audio file used for replacing profanity
            censorship_threshold: Threshold for word censorship (0 to 1)
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model ({model_size}) on {self.device}...")
        self.model = whisper.load_model(model_size).to(self.device)

        self.replacement_sound = AudioSegment.from_file(replacement_sound_path)
        profanity.load_censor_words()
        self.censorship_threshold = censorship_threshold

    def process_audio(self, input_audio_path: str) -> Tuple[AudioSegment, List[Dict]]:
        """
        Process audio file to detect and replace profanity using Whisper.

        Args:
            input_audio_path: Path to input audio file

        Returns:
            Tuple containing processed audio and list of detected profanity
        """
        audio = AudioSegment.from_file(input_audio_path)
        text_segments = self._transcribe_audio(input_audio_path)
        profanity_instances = self._detect_profanity(text_segments)
        processed_audio = self._replace_profanity(audio, profanity_instances)

        return processed_audio, profanity_instances

    def _transcribe_audio(self, audio_path: str) -> List[Dict]:
        """
        Transcribe audio using Whisper with word-level timestamps.

        Args:
            audio_path: Path to audio file

        Returns:
            List of dictionaries containing words and their timestamps
        """
        result = self.model.transcribe(
            audio_path,
            word_timestamps=True,
            language="en"
        )

        segments = []
        for segment in result["segments"]:
            if "words" in segment:
                for word_info in segment["words"]:
                    segments.append({
                        "word": word_info["word"].strip().lower(),
                        "start_time": word_info["start"],
                        "end_time": word_info["end"]
                    })

        return segments

    def _detect_profanity(self, text_segments: List[Dict]) -> List[Dict]:
        """
        Detect profanity in transcribed text.

        Args:
            text_segments: List of transcribed text segments with timestamps

        Returns:
            List of dictionaries containing detected profanity and their locations
        """
        profanity_instances = []

        for segment in text_segments:
            word = segment['word']
            if profanity.contains_profanity(word):
                profanity_instances.append({
                    'word': word,
                    'start_time': segment['start_time'],
                    'end_time': segment['end_time'],
                    'censored_text': profanity.censor(word)
                })

        return profanity_instances

    def _replace_profanity(self, audio: AudioSegment,
                           profanity_instances: List[Dict]) -> AudioSegment:
        """
        Replace detected profanity with replacement sound.

        Args:
            audio: Original audio segment
            profanity_instances: List of detected profanity with timestamps

        Returns:
            Processed audio with replaced profanity
        """
        profanity_instances.sort(key=lambda x: x['start_time'])

        for instance in profanity_instances:
            start_ms = int(instance['start_time'] * 1000)
            end_ms = int(instance['end_time'] * 1000)

            duration = end_ms - start_ms
            adjusted_replacement = self.replacement_sound[:duration]
            adjusted_replacement = adjusted_replacement.fade_in(20).fade_out(20)

            audio = audio[:start_ms] + adjusted_replacement + audio[end_ms:]

        return audio

    def save_report(self, profanity_instances: List[Dict], output_path: str):
        """
        Save a detailed report of detected profanity.

        Args:
            profanity_instances: List of detected profanity instances
            output_path: Path to save the report
        """
        with open(output_path, 'w') as f:
            f.write("Audio Content Moderation Report\n")
            f.write("=" * 30 + "\n\n")

            if not profanity_instances:
                f.write("No profanity detected in the audio.\n")
                return

            f.write(f"Total instances found: {len(profanity_instances)}\n\n")

            for idx, instance in enumerate(profanity_instances, 1):
                f.write(f"Instance {idx}:\n")
                f.write(f"Word: {instance['word']}\n")
                f.write(f"Censored Version: {instance['censored_text']}\n")
                f.write(f"Timestamp: {instance['start_time']:.2f}s - {instance['end_time']:.2f}s\n")
                f.write("-" * 20 + "\n")


def main():
    """Example usage of the AudioContentModerator class."""
    moderator = AudioContentModerator(
        replacement_sound_path="beep.mp3",
        model_size="base"
    )

    processed_audio, profanity_instances = moderator.process_audio("input.mp3")
    processed_audio.export("output.mp3", format="mp3")
    moderator.save_report(profanity_instances, "moderation_report.txt")

    print("Processing complete. Check moderation_report.txt for details.")


if __name__ == "__main__":
    main()
