from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Signal

class Card(QFrame):
  clicked = Signal()

  def __init__(self, title):
    super().__init__()

    self.setProperty("type", "card")
    self.setObjectName("card")

    layout = QVBoxLayout(self)

    title_label = QLabel(title)

    layout.addWidget(title_label)

  def mousePressEvent(self, event):
        self.clicked.emit()