"""Voice activity detection — filters out silence before it reaches STT."""

import numpy as np
import webrtcvad


class VoiceActivityDetector:
    def __init__(self, aggressiveness: int = 2):
        """aggressiveness: 0 (least aggressive filtering) to 3 (most aggressive)."""
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, chunk: np.ndarray, sample_rate: int = 16000) -> bool:
        return self.vad.is_speech(chunk.tobytes(), sample_rate)
