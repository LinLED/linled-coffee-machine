from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ToggleButton(QCheckBox):
    def __init__(
        self,
        width=60,
        bg_color="#777",
        circle_color="#  ",
        active_color="#008cff",
        animation_curve=QEasingCurve.OutQuint,
    ):
        QCheckBox.__init__(self)

        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        # ANIMATION
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)  # Time in miliseconds

        self.stateChanged.connect(self.start_transitioning)

    # CREATE NEW SET AND GET PROPERTIE
    @Property(float)  # get
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transitioning(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)

        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        # SET PAINTER
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # SET AS NO PEN
        p.setPen(Qt.NoPen)

        # Draw RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())

        # CHECK IF IT IS CHECKED
        if not self.isChecked():
            # DRAW BG
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(
                0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
            )

            # DRAW CIRCLE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)
        else:
            # DRAW BG
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(
                0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
            )

            # DRAW CIRCLE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)

        p.end()
