from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from components.my_widget import MyWidget


class IdleScene(MyWidget):
    def __init__(self):
        super().__init__()
        self._textAlpha = 255
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        layout = QVBoxLayout(self)
        self.title = QLabel("LINLED COFFEE MACHINE\nFor demonstration purpose only\n\nBring your hand to interact")
        self.title.setStyleSheet("color: rgba(219, 193, 172, 255);")
        self.title.setMouseTracking(True)

        self.font = QFont("Arial", 72)
        self.title.setFont(self.font)

        # Center align the title
        self.title.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)

        # Create the animation
        self.animation = QPropertyAnimation(self, b"textAlpha")
        self.animation.setDuration(4000)  # Duration in milliseconds
        self.animation.setStartValue(255)  # Start from opaque
        self.animation.setEndValue(-255)  # End at semi-transparent
        self.animation.setLoopCount(100000)  # Infinite loop

        # Connect the finished signal to a slot to reverse the direction
        self.animation.start()

    @Property(int)
    def textAlpha(self):
        return self._textAlpha

    @textAlpha.setter
    def textAlpha(self, alpha):
        self._textAlpha = abs(alpha)
        self.title.setStyleSheet(f"color: rgba(219, 193, 172, {abs(alpha)});")

    def reverseAnimationDirection(self):
        if self.animation.direction() == QAbstractAnimation.Forward:
            self.animation.setDirection(QAbstractAnimation.Backward)
        else:
            self.animation.setDirection(QAbstractAnimation.Forward)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.main_window.mouseMoveEvent(event)
