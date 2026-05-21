from PySide6.QtWidgets import QWidget, QHBoxLayout

import os
from pathlib import Path

from src.config import Config
from src.ui.card import Card
from src.ui.audio_player import AudioStreamer

config = Config()

class FileCard(Card):
  def __init__(self, title, file_path):
    super().__init__(title)
    self.file_path = file_path
    
    # Create an audio streamer specifically for this card
    self.audio_streamer = AudioStreamer(self)

    self.clicked.connect(self.on_click)

  def on_click(self):
    print(f"Playing: {self.file_path}")
    self.audio_streamer.play_sound(self.file_path)

class FilesView(QWidget):
  def __init__(self):
    super().__init__()

    path = Path(config.files_path)
    layout = QHBoxLayout(self)

    try:
      files = os.listdir(path)
      
      for file in files:
        file_path = str(path / file)
        fileCard = FileCard(file, file_path)
        layout.addWidget(fileCard)
    
    except FileNotFoundError:
      print(f"files not found: {path}")
