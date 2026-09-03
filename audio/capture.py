"""Microphone capture via sounddevice — yields raw audio chunks for VAD/STT."""

from collections.abc import Iterator

import numpy as np
import sounddevice as sd


def stream_microphone(sample_rate: int = 16000, chunk_ms: int = 30) -> Iterator[np.ndarray]:
    """Yield audio chunks from the default input device, resampled to sample_rate."""
    device_info = sd.query_devices(kind="input")
    native_rate = int(device_info["default_samplerate"])
    native_chunk_frames = int(native_rate * chunk_ms / 1000)

    # capture at the device's native rate — some reject unsupported rates
    with sd.InputStream(samplerate=native_rate, channels=1, dtype="int16") as stream:
        while True:
            data, overflowed = stream.read(native_chunk_frames)
            data = data.flatten()
            if native_rate != sample_rate:
                data = _resample(data, native_rate, sample_rate)
            yield data.astype(np.int16)


def _resample(audio: np.ndarray, orig_rate: int, target_rate: int) -> np.ndarray:
    target_len = int(len(audio) * target_rate / orig_rate)
    return np.interp(
        np.linspace(0, len(audio), target_len, endpoint=False),
        np.arange(len(audio)),
        audio,
    )
