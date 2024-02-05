from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtWidgets import *

from components.style import COFFEE_COLOR
from components.assets import resource_path

VALIDATION_TIME = 200


class ValidateBottomZone(QWidget):
    validate_signal = Signal()

    def __init__(self):
        super().__init__()
        self.init_font()
        self.init_ui()
        self.setupAnimation()
        self.elapsedTimer = QElapsedTimer()

    def init_font(self):
        self.font_db = QFontDatabase()
        self.font_id = self.font_db.addApplicationFont(
        resource_path("assets/fonts/arlrdbd.ttf")
      )
        if self.font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        else:
            print("Failed to load and register the custom font.")

    def init_ui(self):
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("↓ Go down to validate ↓")
        self.font = QFont(self.font_family, 48)
        self.label.setFont(self.font)
        self.label.setContentsMargins(0, 0, 0, 0)

        self.container_layout.addWidget(self.label, Qt.AlignCenter, Qt.AlignCenter)
        self.setMinimumHeight(100)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.set_default_style()

    def setupAnimation(self):
        self._textAlpha = 255
        self.animation = QPropertyAnimation(self, b"bgColor")
        self.animation.setDuration(VALIDATION_TIME)  # Duration in milliseconds
        self.animation.setStartValue(QColor(99, 72, 50, 128))
        self.animation.setEndValue(QColor(219, 193, 172, 255))  # Lighter color
        self.animation.finished.connect(self.on_animation_finished)

        self.glowing_animation = QPropertyAnimation(self, b"textAlpha")
        self.glowing_animation.setStartValue(255)  # Start from opaque
        self.glowing_animation.setEndValue(-255)  # End at semi-transparent
        self.glowing_animation.setDuration(2000)  # Duration in milliseconds
        self.glowing_animation.finished.connect(self.on_glowing_animation_finished)

    def set_default_style(self):
        self.label.setStyleSheet(
            f"border: 0px; background-color: transparent; color: {COFFEE_COLOR[0]};"
        )
        self.container.setStyleSheet(
          f"border: 0px; background-color: transparent;"
        )

    def set_debug_style(self):
        self.label.setStyleSheet(
            f"border: 0px; background-color: transparent; color: {COFFEE_COLOR[0]};"
        )
        self.container.setStyleSheet(
            "border: 3px solid red; background-color: rgba(99, 72, 50, 128);"
        )

    def _set_bg_color(self, color):
        style = f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});"
        self.container.setStyleSheet(style)

    def _get_bg_color(self):
        return self.container.palette().color(self.container.backgroundRole())

    def on_glowing_animation_finished(self):
        QTimer.singleShot(500, lambda: self.glowing_animation.start())

    @Property(QColor, fset=_set_bg_color, fget=_get_bg_color)
    def bgColor(self):
        return self._get_bg_color()

    def showEvent(self, event):
        self.set_default_style()
        self.glowing_animation.start()

    def enterEvent(self, event):
        self.glowing_animation.stop()
        self.container.setStyleSheet(
            "border-top: 3px solid #ece0d1; background-color: rgba(99, 72, 50, 128);"
        )
        self.label.setStyleSheet(
            "border: 0px; background-color: transparent; color: #ece0d1;"
        )
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.stop()
        self.glowing_animation.start()
        self.set_default_style()

    def on_animation_finished(self):
        self.parent().validate_card()      

    @Property(int)
    def textAlpha(self):
        return self._textAlpha

    @textAlpha.setter
    def textAlpha(self, alpha):
        self._textAlpha = abs(alpha)
        self.label.setStyleSheet(f"color: rgba(219, 193, 172, {abs(alpha)});")
