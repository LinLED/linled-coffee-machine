from PySide6.QtCore import *
from PySide6.QtMultimedia import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from components.utils import findMainWindow, Debug
from components.assets import sound_path

ANIMATION_SPEED = 200
DEFAULT_MARGINS = 50
ELAPSED_TIMER = 100
QUICK_MOVE_THRESHOLD = 150

class InteractiveCard(QWidget):
    def __init__(self, parent=None):
        super().__init__()

    def quick_move_detection(self, event):
        if not self.main_window.params.movement_validation.state:
            if self.elapsedTimer.elapsed() > ELAPSED_TIMER:
                currentMousePosition = event.globalPosition().toPoint()
                movement = currentMousePosition - self.lastMousePosition

                if (
                    movement.y() > abs(movement.x())
                    and movement.y() > QUICK_MOVE_THRESHOLD
                ):
                    self.validate_card()

                self.lastMousePosition = currentMousePosition
                self.elapsedTimer.restart()


    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def validate_card(self):
        pass