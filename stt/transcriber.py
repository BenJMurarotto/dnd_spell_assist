"""Speech-to-text via faster-whisper.

Runs locally (no network round trip). Uses initial_prompt to bias
transcription toward D&D spell vocabulary — Whisper will otherwise
mishear proper nouns like spell names.
"""

from collections.abc import Iterable
from faster_whisper import WhisperModel
import numpy as np


class Transcriber:
    def __init__(self, model_size: str = "small.en", spell_names: list[str] | None = None):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.spell_names = spell_names

    def transcribe_chunk(self, audio_chunks: Iterable[np.ndarray]) -> str:
        """Transcribe a buffered window of audio chunks and return the text."""
        combined = np.concatenate(list(audio_chunks))
        audio_float = combined.astype(np.float32) / 32768.0
        prompt = ", ".join(self.spell_names) if self.spell_names else None
        segments, _ = self.model.transcribe(audio_float, initial_prompt=prompt)
        return " ".join(segment.text for segment in segments)
