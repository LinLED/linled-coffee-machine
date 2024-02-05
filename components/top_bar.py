import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from config import BASIC_FONT, TOP_BAR_SPEED
from components.utils import custom_font, get_app_dimensions, Debug
from components.parameters import GlobalParameters
from components.assets import resource_path
from components.style import COFFEE_COLOR


class TopBarProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.initParams()
        self.initAnimation()

    def initParams(self):
        self._progress = 0.0

    def initAnimation(self):
        self.animation = QPropertyAnimation(self, b"progress")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def setProgress(self, progress, animation_time):
        # Start an animation from the current progress value to the new value
        self.animation.stop()
        self.animation.setDuration(animation_time)  # Duration in milliseconds
        self.animation.setStartValue(self._progress)
        self.animation.setEndValue(progress)
        self.animation.start()

    def getProgress(self):
        return self._progress

    @Property(float)
    def progress(self):
        return self.getProgress()

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height() / 4, QColor("#ece0d1"))

        # Draw progress rectangle
        progress_rect = QRect(0, 0, self.width() * self._progress, self.height() / 4)
        fill_color = QColor("#38220f")
        painter.fillRect(progress_rect, fill_color)


class TopBar(QWidget, Debug):
    labels = ["Selection", "Option", "Cart", "Payment", "Preparation"]

    def __init__(self, state):
        super().__init__()
        self.initParams(state)
        self.initUI(state)
        self.addLabels()
        self.addProgressBar()
        if GlobalParameters.getInstance().debug.state:
            self.apply_debug_style()

    def initParams(self, state):
        self.state = state
        self.side_margin = 0.05 * get_app_dimensions(self).width

    def initUI(self, state):
        # Main container
        self.main_layout = QVBoxLayout(self)  # Main layout is vertical
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # IMPORTANT

    def addLabels(self):
        self.labels_layout = QHBoxLayout()  # Layout for labels
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont(resource_path("assets/fonts/arlrdbd.ttf"))
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("Failed to load and register the custom font.")

        self.font = QFont(font_family, 24)

        for id, text in enumerate(self.labels):
            label = QLabel(text)
            self.font.setBold(id == self.state)
            label.setFont(self.font)
            label.setStyleSheet("color: #dbc1ac; text-align: left;")
            self.labels_layout.addWidget(label)

        self.main_layout.addLayout(self.labels_layout)  # Add labels layout to container

    def addProgressBar(self):
        self.progressBar = TopBarProgress()
        self.progressBar.setFixedHeight(40)  # Set a fixed height for the progress bar
        self.progressBar.setStyleSheet(
            "QProgressBar {background-color: #dbc1ac; border: border-radius: 2px;}"
            "QProgressBar::chunk {background-color: #38220f; border-radius: 2px;}"
        )
        self.progressBar.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.progressBar)

    def set_state(self, state: int, animation_time=TOP_BAR_SPEED):
        self.progressBar.setProgress((state * 20) / 100, animation_time)
