from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from components.utils import findMainWindow


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)
        super().showEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
