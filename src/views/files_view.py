from PySide6.QtWidgets import QWidget, QHBoxLayout

import os
from pathlib import Path

from src.config import Config

from src.ui.card import Card

config = Config()

class FileCard(Card):
  def __init__(self, title):
    super().__init__(title)



class FilesView(QWidget):
  def __init__(self):
    super().__init__()

    path = Path(config.files_path)
    layout = QHBoxLayout(self)

    try:
      files = os.listdir(path)
      
      for file in files:
        fileCard = FileCard(file)
        layout.addWidget(fileCard)
    
    except FileNotFoundError:
      print(f"files not found: {path}")



    
