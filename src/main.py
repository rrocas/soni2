import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider
)

from PySide6.QtCore import Qt

class Window(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("soni2 - beta")

app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())

