"""Main PySide6 window — spell display panel.

Receives ListenerWorker.spell_detected signals and renders the looked-up
spell data (description, level, casting time, etc.).
"""

from PySide6.QtWidgets import QLabel, QMainWindow, QTextEdit, QVBoxLayout, QWidget

from ui.worker import ListenerWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D Spell Assist")
        self.resize(500, 400)

        self.name_label = QLabel("Listening...")
        self.name_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.meta_label = QLabel("")

        self.desc_box = QTextEdit()
        self.desc_box.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.meta_label)
        layout.addWidget(self.desc_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.worker = ListenerWorker()
        self.worker.spell_detected.connect(self.display_spell)
        self.worker.start()

    def display_spell(self, spell: dict) -> None:
        self.name_label.setText(spell["name"])
        self.meta_label.setText(
            f"Level {spell.get('level')} | "
            f"{spell.get('school', {}).get('name', '')} | "
            f"Casting Time: {spell.get('casting_time', '')} | "
            f"Range: {spell.get('range', '')} | "
            f"Duration: {spell.get('duration', '')}"
        )
        self.desc_box.setPlainText("\n\n".join(spell.get("desc", [])))

    def closeEvent(self, event) -> None:
        self.worker.stop()
        self.worker.wait()
        event.accept()
