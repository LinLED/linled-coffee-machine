import sys
from collections import namedtuple
from dataclasses import dataclass, field

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from components.parameters import GlobalParameters


def findMainWindow(widget: QWidget):
    while widget is not None:
        if isinstance(widget, QMainWindow):
            return widget
        widget = widget.parent()


Dimensions = namedtuple("Dimensions", ["width", "height"])


def get_app_dimensions(widget: QWidget):
    screen = QApplication.primaryScreen()
    rect = screen.geometry()

    if rect is not None:
        return Dimensions(width=rect.width(), height=rect.height())
    else:
        return None


class Debug:
    def apply_debug_style(self):
            self.setStyleSheet("border: 2px solid red;")  # Example debug style


# font_id = QFontDatabase.addApplicationFont(
#     "assets/fonts/IFBombergSans-Regular-Text.ttf"
# )

# font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

custom_font = QFont("Times")
