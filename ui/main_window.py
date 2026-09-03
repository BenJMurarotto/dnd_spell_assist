"""Main PySide6 window — renders spell data from ListenerWorker.spell_detected."""

from PySide6.QtWidgets import QLabel, QMainWindow, QTextEdit, QVBoxLayout, QWidget

from ui.worker import ListenerWorker


ARCANE_STYLE = """
    QWidget#container {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                     stop:0 #1a1533, stop:1 #100c22);
    }
    QLabel#nameLabel {
        color: #e6e1f5;
        font-size: 24px;
        font-weight: bold;
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        padding-bottom: 6px;
        border-bottom: 2px solid #7c5cff;
    }
    QLabel#metaLabel {
        color: #9d93c9;
        font-size: 12px;
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        padding-top: 4px;
        padding-bottom: 4px;
    }
    QTextEdit#descBox {
        background-color: #1e1840;
        color: #d8d3f0;
        border: 1px solid #4a3f80;
        border-radius: 6px;
        padding: 10px;
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 13px;
        selection-background-color: #4fd6d6;
        selection-color: #100c22;
    }
    QTextEdit#descBox:focus {
        border: 1px solid #4fd6d6;
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D Spell Assist")
        self.resize(500, 400)

        self.name_label = QLabel("Cast A Spell...")
        self.name_label.setObjectName("nameLabel")

        self.meta_label = QLabel("")
        self.meta_label.setObjectName("metaLabel")

        self.desc_box = QTextEdit()
        self.desc_box.setObjectName("descBox")
        self.desc_box.setReadOnly(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)
        layout.addWidget(self.name_label)
        layout.addWidget(self.meta_label)
        layout.addWidget(self.desc_box)

        container = QWidget()
        container.setObjectName("container")
        container.setLayout(layout)
        container.setStyleSheet(ARCANE_STYLE)
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
