"""QThread wrapper around pipeline.listener.SpellListener.

The only place in the app that touches both the pipeline and Qt. Turns
the pipeline's plain callback into a Qt signal so the GUI thread never
blocks on audio capture or STT inference.
"""

from PySide6.QtCore import QThread, Signal
from pipeline.listener import SpellListener

class ListenerWorker(QThread):
    spell_detected = Signal(dict)

    def run(self) -> None:
        self.listener = SpellListener(on_spell_detected=self.spell_detected.emit)
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()