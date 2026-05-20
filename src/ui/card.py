from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

class Card(QFrame):
  def __init__(self, title):
    super().__init__()

    self.setProperty("type", "card")
    self.setObjectName("card")

    layout = QVBoxLayout(self)

    title_label = QLabel(title)

    layout.addWidget(title_label)