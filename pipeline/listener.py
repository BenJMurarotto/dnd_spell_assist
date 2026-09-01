"""Orchestrates capture -> VAD -> STT -> match -> callback.

Deliberately has zero knowledge of Qt or threading, so it can be run and
tested from a plain script (see scripts/test_lookup_cli.py-style checks)
before being wrapped for the GUI in ui/worker.py.
"""

from collections.abc import Callable
from audio.capture import stream_microphone
from audio.vad import VoiceActivityDetector
from data.loader import load_spells
from matching.spell_matcher import SpellMatcher
from stt.transcriber import Transcriber

class SpellListener:
    def __init__(self, on_spell_detected: Callable[[dict], None], silence_chunks_to_end_utterance: int = 15):
        """on_spell_detected is called with a spell dict each time one is matched."""
        self.silence_chunks_to_end_utterance = silence_chunks_to_end_utterance
        self.on_spell_detected = on_spell_detected
        self.spells = load_spells()
        self.vad = VoiceActivityDetector(aggressiveness=1)
        spell_names = [spell["name"] for spell in self.spells.values()]
        self.transcriber = Transcriber(spell_names=spell_names)
        self.matcher = SpellMatcher(spell_names=spell_names)
        self._running = False


    def start(self) -> None:
        """Begin the capture -> VAD -> STT -> match loop. Blocking."""
        self._running = True
        buffer = []
        silence_count = 0

        for chunk in stream_microphone():
            if not self._running:
                break
            if self.vad.is_speech(chunk):
                buffer.append(chunk)
                silence_count = 0
            elif buffer:
                silence_count += 1
                if silence_count > self.silence_chunks_to_end_utterance:
                    transcript = self.transcriber.transcribe_chunk(buffer)
                    print(f"heard: {transcript!r}")
                    for name in self.matcher.find_matches(transcript):
                        spell = self.spells[name.lower()]
                        self.on_spell_detected(spell)
                    buffer = []
                    silence_count = 0


    def stop(self) -> None:
        self._running = False
