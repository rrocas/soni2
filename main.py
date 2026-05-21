import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QFileDialog
)
from src.views import files_view
from src.shared.styles import load_qss

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("soni2 - alpha version")
        self.setObjectName("mainWindow")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.resize(300, 200)

        self.btn_folder = QPushButton("📁 Select folder")
        self.btn_folder.clicked.connect(self.open_folder)
        self.mainLayout.addWidget(self.btn_folder)

        self.FilesView = files_view.FilesView()
        self.mainLayout.addWidget(self.FilesView)

        self.setStyleSheet(load_qss("src/styles"))

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if folder:
            self.FilesView.load_folder(folder)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())