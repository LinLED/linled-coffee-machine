from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from components.toggle_button import ToggleButton
from components.parameters import GlobalParameters, Parameter

from config import CURSOR_HIDDEN


class OptionParameter(QWidget):
    def __init__(self, parameter: Parameter):
        super().__init__()
        self.parameter = parameter
        self.initUI()  # Pass toggle_changed to initUI

    def initUI(self):
        self.container = QWidget()
        self.container.setStyleSheet("border: 2px solid black;")
        self.layout = QHBoxLayout(self.container)
        self.parameter_label = QLabel(self.parameter.display_name)
        self.parameter_label.setStyleSheet("color: rgba(219, 193, 172, 255);")
        # Set the font size to 64
        font = QFont()
        font.setPointSize(22)  # Set the font size
        self.parameter_label.setFont(font)

        self.toggle_button = ToggleButton()

        self.layout.addWidget(self.parameter_label, Qt.AlignCenter, Qt.AlignCenter)
        self.layout.addWidget(self.toggle_button, Qt.AlignCenter, Qt.AlignCenter)

        self.toggle_button.stateChanged.connect(
            lambda: self.updateParameter(self.toggle_button.isChecked())
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.container)
        self.container.setStyleSheet("border: 0px;")

    def updateParameter(self, state):
        self.parameter.state = state


class OptionsScene(QWidget):
    def __init__(self, parameters: GlobalParameters):
        super().__init__()
        self.cursor_display = CURSOR_HIDDEN
        self.global_parameters = parameters
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.addTitle("Options")
        for key, parameter in vars(self.global_parameters).items():
            self.addParameter(parameter)

    def addTitle(self, title: str):
        title = QLabel("Options")
        # Set the font size to 64
        font = QFont("Arial", 48)
        title.setFont(font)
        title.setStyleSheet("color: #ece0d1; border: 0px;")

        self.layout.addWidget(title, Qt.AlignTop, Qt.AlignCenter)
        self.layout.setContentsMargins(0, 50, 0, 0)

    def addParameter(self, parameter: Parameter) -> OptionParameter:
        parameter = OptionParameter(parameter)
        self.layout.addWidget(parameter, Qt.AlignCenter, Qt.AlignCenter)

    def showEvent(self, event):
        QApplication.restoreOverrideCursor()  # Show cursor

    def hideEvent(self, event):
        if self.global_parameters.cursor_hidden.state:
            QApplication.setOverrideCursor(Qt.BlankCursor)  # Hide cursor
