from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ProgressionBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout
        self.layout = QVBoxLayout(self)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(False)  # Hide text
        self.progress_bar.setStyleSheet(
            "QProgressBar {border: 2px solid grey; border-radius: 5px;}"
            "QProgressBar::chunk {background-color: #05B8CC;}"
        )
        self.layout.addWidget(self.progress_bar)

        # Timer for Progress Bar Update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(16)  # Update interval in milliseconds

        # Initialize progress value
        self.progress_value = 0

    def update_progress_bar(self):
        # Check if the progress bar is visible
        if not self.progress_bar.isVisible():
            return

        self.progress_value += 1  # Increment the progress
        self.progress_bar.setValue(self.progress_value)

        # Reset if maximum is reached
        if self.progress_value >= 100:
            self.progress_value = 0
            self.progress_bar.setValue(self.progress_value)
            self.parent().parent().parent().set_scene(1)
