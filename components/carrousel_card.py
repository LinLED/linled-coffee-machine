import os
from enum import Enum

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import QSoundEffect

from config import BASIC_FONT, ANIMATION_SPEED

from components.assets import resource_path
from components.parameters import GlobalParameters
from components.scenes import Scenes
from components.utils import findMainWindow, get_app_dimensions, custom_font, Debug
from components.selection import CoffeeType, Selection


DEFAULT_MARGIN = 70
SELECTED_MARGIN = 30
VALIDATED_MARGIN = 40
ELAPSED_TIMER = 200
QUICK_MOVE_THRESHOLD = 100


class CarrouselCard(QWidget, Debug):
    card_validation_signal = Signal(CoffeeType)

    def __init__(self, coffee_type: CoffeeType):
        super().__init__()
        self.main_window = findMainWindow(self)
        self.init_params(coffee_type)
        self.init_animations()
        self.init_font()
        self.init_ui()
        self.elapsedTimer = QElapsedTimer()
        if GlobalParameters.getInstance().debug.state:
            self.apply_debug_style()
        self.elapsedTimer.start()
        self.lastMousePosition = QCursor.pos()

    def init_params(self, coffee_type):
        self._font_size = 16
        self._margins = DEFAULT_MARGIN
        self.coffee_type = coffee_type

        self.active = False
        self.animated = True
        self.selected = False
        self.validated = False

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
        self.init_label()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label, 0, Qt.AlignTop | Qt.AlignHCenter)

        self.set_default_style()

    def init_label(self):
        self.label = QLabel(self.coffee_type.name)
        self.label.setFont(QFont(self.font_family, 24))
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.label.setStyleSheet("border: 0px; background-color: transparent;")
        self.set_background_image(resource_path(self.coffee_type.image_path))

    def set_fallback_background(self):
        # Set a default background color or a placeholder image
        self.setStyleSheet(
            "QWidget { background-color: #CCCCCC; }"
        )  # Example: light gray background

    def set_background_image(self, imagePath):
        self.backgroundPixmap = QPixmap(imagePath)
        if self.backgroundPixmap.isNull():
            print(f"Failed to load image: {imagePath}")
            return
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # Adjust the rect to account for margins
        margins = self.contentsMargins()
        adjustedRect = rect.adjusted(
            margins.left(), margins.top(), -margins.right(), -margins.bottom()
        )

        if not self.backgroundPixmap.isNull():
            painter.drawPixmap(adjustedRect, self.backgroundPixmap)

            if self.selected:
                # Draw a border around the pixmap
                border_width = 5
                border_color = QColor("#dbc1ac")
                pen = QPen(border_color, border_width)
                painter.setPen(pen)
                painter.drawRect(
                    adjustedRect.adjusted(
                        border_width // 2,
                        border_width // 2,
                        -border_width // 2,
                        -border_width // 2,
                    )
                )

        super().paintEvent(event)

    def updateStylesheet(self):
        style_string = "; ".join(
            [f"{key}: {value}" for key, value in self.style_sheet.items()]
        )
        self.setStyleSheet(f"QWidget {{ {style_string} }}")

    def showEvent(self, event):
        self.main_window = findMainWindow(self)

    def enterEvent(self, event):
        if self.active:
            self.setMouseTracking(True)
            self.select()
        else:
            pass

    def select(self):
        self.main_window.change_sound.play()
        self.selected = True
        self.set_selected_style()
        if self.animated:
            self.start_margin_animation(DEFAULT_MARGIN, SELECTED_MARGIN)
            self.start_text_animation(24, 24)

        self.parent().parent().parent().parent().current_coffee_type = self.coffee_type
        self.parent().parent().parent().parent().unselect_cards(self)

    def leaveEvent(self, event):
        self.setMouseTracking(False)

    def unselect(self):
        if self.selected and self.animated:
            self.start_text_animation(24, 24)
            self.start_margin_animation(SELECTED_MARGIN, DEFAULT_MARGIN)
        self.selected = False
        self.set_default_style()

    def validate_card(self):
        self.set_validated_style()
        self.main_window.validation_sound.play()
        self.card_validation_signal.emit(self.coffee_type)
        self.font_size = 18

    def set_default_style(self):
        self.setStyleSheet(
            "background-color: rgba(219,193,172, 128); border: 2px solid red;"
        )
        self.margins = DEFAULT_MARGIN
        self.label.setStyleSheet("border: 2px solid black;")

        if self.main_window != None:
            if self.main_window.params.debug.state:
                self.setStyleSheet(
                    "background-color: rgba(219,193,172, 128); border: 2px solid red;"
                )
                self.label.setStyleSheet("border: 2px solid red;")

    def set_selected_style(self):
        if self.main_window.params.debug.state:
            self.setStyleSheet("border: 2px solid yellow;")
        else:
            self.setStyleSheet(
                "background-color: rgba(219,193,172, 255); border: 2px solid red;"
            )

    def set_validated_style(self):
        self.margins = VALIDATED_MARGIN

    def hideEvent(self, event):
        super().hideEvent(event)
        self.selected = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if (
            self.main_window.params.movement_validation.state
            or self.main_window.params.carrousel_swipe.state
        ):
            currentMousePosition = event.globalPosition().toPoint()
            if self.elapsedTimer.elapsed() < ELAPSED_TIMER:
                movement = currentMousePosition - self.lastMousePosition

                # Detect vertical swipe (up or down)
                if (
                    self.main_window.params.movement_validation.state
                    and movement.y() > abs(movement.x())
                    and movement.y() > QUICK_MOVE_THRESHOLD
                ):
                    self.validate_card()
                    self.disableMouseTrackingForPause()

            self.lastMousePosition = currentMousePosition

        self.elapsedTimer.restart()

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def disableMouseTrackingForPause(self):
        self.setMouseTracking(False)
        QTimer.singleShot(500, lambda: self.setMouseTracking(True))

    # ANIMATIONS
    def init_animations(self):
        self.init_text_animation()
        self.init_margin_animation()

    def init_text_animation(self):
        self.text_animation = QPropertyAnimation(self, b"font_size")
        self.text_animation.setDuration(ANIMATION_SPEED)

    def init_margin_animation(self):
        self.margin_animation = QPropertyAnimation(self, b"margins")
        self.margin_animation.setDuration(ANIMATION_SPEED)

    def start_text_animation(self, start, end):
        self.text_animation.stop()
        self.text_animation.setStartValue(start)
        self.text_animation.setEndValue(end)
        self.text_animation.start()

    def start_margin_animation(self, start, end):
        self.margin_animation.stop()
        self.margin_animation.setStartValue(start)
        self.margin_animation.setEndValue(end)
        self.margin_animation.start()

    # PROPERTIES

    @Property(int)
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self.label.setFont(QFont(self.font_family, value))

    @Property(int)
    def margins(self):
        return self._margins

    @margins.setter
    def margins(self, value):
        self._margins = value
        self.setContentsMargins(int(value / 1.62), value, int(value / 1.62), value)
