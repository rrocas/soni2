from PySide6.QtWidgets import QWidget, QVBoxLayout
import os
from pathlib import Path

from src.ui.card import Card
from src.audio.audio_player import AudioStreamer

_audio_streamer = None

def get_audio_streamer():
    global _audio_streamer
    if _audio_streamer is None:
        _audio_streamer = AudioStreamer()
    return _audio_streamer


class FileCard(Card):
    def __init__(self, title, file_path):
        super().__init__(title)
        self.file_path = file_path
        self.audio_streamer = get_audio_streamer()
        self.clicked.connect(self.on_click)

    def on_click(self):
        print(f"Playing: {self.file_path}")
        self.audio_streamer.play_sound(self.file_path)


class FilesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.layout_ = QVBoxLayout(self)

    def load_folder(self, folder_path):
        self.current_path = Path(folder_path)
        self.refresh()

    def refresh(self):
        while self.layout_.count():
            item = self.layout_.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            for file in os.listdir(self.current_path):
                if Path(file).suffix.lower() in ('.mp3', '.wav', '.ogg', '.flac'):
                    file_path = str(self.current_path / file)
                    self.layout_.addWidget(FileCard(file, file_path))
        except FileNotFoundError:
            print(f"Folder not found: {self.current_path}")