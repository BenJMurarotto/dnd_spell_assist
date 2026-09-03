"""Speech-to-text via faster-whisper, run locally. initial_prompt biases transcription toward spell names since Whisper otherwise mishears them."""

import sys
from collections.abc import Iterable
from pathlib import Path

from faster_whisper import WhisperModel
import numpy as np


def _resolve_model_path(model_size: str) -> str:
    """Prefer a locally bundled CT2 model (offline packaged builds); else fall back to HF Hub download."""
    base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent.parent
    bundled = base / "models" / f"{model_size}_ct2"
    return str(bundled) if bundled.is_dir() else model_size


class Transcriber:
    def __init__(self, model_size: str = "tiny.en", spell_names: list[str] | None = None):
        model_path = _resolve_model_path(model_size)
        self.model = WhisperModel(model_path, device="cpu", compute_type="int8", cpu_threads=4)
        self.spell_names = spell_names

    def transcribe_chunk(self, audio_chunks: Iterable[np.ndarray]) -> str:
        """Transcribe a buffered window of audio chunks and return the text."""
        combined = np.concatenate(list(audio_chunks))
        audio_float = combined.astype(np.float32) / 32768.0
        prompt = ", ".join(self.spell_names) if self.spell_names else None
        segments, _ = self.model.transcribe(audio_float, initial_prompt=prompt, temperature=0.0)
        return " ".join(segment.text for segment in segments)
