from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from components.top_bar import TopBar
from components.carrousel import Carrousel
from components.utils import findMainWindow
from components.validate_bottom import ValidateBottomZone


class CoffeeSelectionScene(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.validate_bottom_zone = None

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.carrousel = Carrousel()
        self.carrousel.setStyleSheet("border: 2px solid black")
        self.layout.addWidget(self.carrousel)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)
        self.add_bottom_validation()

    def hideEvent(self, event):
        self.removeBottomValidation()

    def add_bottom_validation(self):
        self.validate_bottom_zone = ValidateBottomZone()
        self.validate_bottom_zone.setContentsMargins(0, 0, 0, 0)
        self.validate_bottom_zone.validate_signal.connect(self.validate_card)
        self.layout.addWidget(self.validate_bottom_zone, alignment=Qt.AlignBottom)

    def removeBottomValidation(self):
        if self.validate_bottom_zone is not None:
            self.layout.removeWidget(self.validate_bottom_zone)
            self.validate_bottom_zone.deleteLater()
            self.validate_bottom_zone = None

    def validate_card(self):
        self.carrousel.validate_card()
