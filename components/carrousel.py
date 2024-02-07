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
from components.carrousel_card import CarrouselCard

# Constants
BASIC_FONT = "Arial"  # Replace with your font
ANIMATION_SPEED = 200  # Animation speed inpai milliseconds
NORMAL_FONT_SIZE = 10
ENLARGED_FONT_SIZE = 20
MAX_FONT_SIZE = 32
DEFAULT_MARGINS = 50
QUICK_MOVE_THRESHOLD = 150
CARROUSSEL_CARD_NUMBER = 4


def linear_map(value, in_min, in_max, out_min, out_max):
    if in_min <= value <= in_max:
        return round(
            ((value - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min
        )
    else:
        return out_min  # return out_min by default


class Carrousel(QWidget, Debug):
    def __init__(self):
        super().__init__()
        self.initParams()
        self.initUI()
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.auto_scroll)
        self.scroll_direction = 0  # 0: no scroll, -1: left, 1: right
        self.current_coffee_type = None
        if GlobalParameters.getInstance().debug.state:
            self.apply_debug_style()

        # Enable key events for the widget
        self.setFocusPolicy(Qt.StrongFocus)

    def initParams(self):
        self.number_of_cards = CARROUSSEL_CARD_NUMBER

    def initUI(self):
        # Scroll Area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setStyleSheet("background-color: transparent; border: 0px;")

        # Create a container widget and a layout
        self.container = QWidget()
        self.container.installEventFilter(self)

        self.layout = QHBoxLayout(self.container)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create CarrouselCard for each coffee type and add to the layout
        self.carrousel_cards = [
            CarrouselCard(coffee_type)
            for coffee_type in CoffeeType
            if coffee_type != CoffeeType.NONE
        ]
        for card in self.carrousel_cards:
            card.card_validation_signal.connect(self.on_card_validation)
            card.setMinimumWidth(get_app_dimensions(self).width / self.number_of_cards)
            self.layout.addWidget(card)

        # Set the container as the scroll area's widget

        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.container)

        # Main layout of Carrousel is just the scroll area
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scrollArea)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Connect scroll bar signal
        self.scrollArea.horizontalScrollBar().valueChanged.connect(self.check_scroll)

    def eventFilter(self, obj, event):
        if obj is self.container and event.type() == QEvent.MouseMove:
            self.mouseMoveEvent(event)
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)
        for card in self.carrousel_cards:
            card.set_default_style()
        QTimer.singleShot(1500, lambda: self.activate_cards())
        QTimer.singleShot(1500, lambda: self.container.setMouseTracking(True))
        self.move_last_to_start()

    def activate_cards(self):
        for card in self.carrousel_cards:
            card.active = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.main_window.params.carrousel_swipe.state:
            # Scroll behaviour
            mouse_x = event.globalPosition().toPoint().x()
            widget_x = self.mapToGlobal(self.pos()).x()
            widget_width = self.width()

            # Adjust these thresholds as needed
            left_threshold = widget_x + widget_width * 0.1
            right_threshold = widget_x + widget_width * 0.9

            # Calculate dynamic scroll speed
            scroll_speed = self.calculate_scroll_speed(
                mouse_x, left_threshold, right_threshold
            )
            transparency_mapped = linear_map(scroll_speed, 10, 15, 64, 255)

            if mouse_x < left_threshold:
                self.scroll_direction = -1
                self.scroll_timer.start(30 - scroll_speed)
                self.scrollArea.setStyleSheet(
                    f"border-left: 10px solid rgba(236,224,209, {transparency_mapped}); border-top: none; border-right: none; border-bottom: none; background-color: transparent;"
                )
            elif mouse_x > right_threshold:
                self.scroll_direction = 1
                self.scroll_timer.start(abs(5 - scroll_speed))
                self.scrollArea.setStyleSheet(
                    f"border-right: 10px solid rgba(236,224,209, {transparency_mapped}); border-top: none; border-left: none; border-bottom: none; background-color: transparent;"
                )
            else:
                self.scroll_timer.stop()
                self.scrollArea.setStyleSheet(
                    "border: 0px; background-color: transparent;"
                )

    def calculate_scroll_speed(self, mouse_x, left_threshold, right_threshold):
        # Adjust these factors to fine-tune the responsiveness
        min_speed = 10
        max_speed = 15

        if mouse_x < left_threshold:
            # Closer to the left edge => Faster scroll
            return linear_map(mouse_x, 0, left_threshold, max_speed, min_speed)
        elif mouse_x > right_threshold:
            # Closer to the right edge => Faster scroll
            return linear_map(
                mouse_x, right_threshold, self.width(), min_speed, max_speed
            )
        else:
            # Default speed
            return min_speed

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if self.main_window.params.carrousel_swipe.state:
            if event.key() == Qt.Key_Left:
                self.move_cards_left()
            elif event.key() == Qt.Key_Right:
                self.move_cards_right()
            else:
                super().keyPressEvent(event)

    def move_cards_left(self):
        self.adjust_scroll(-1)

    def move_cards_right(self):
        self.adjust_scroll(1)

    def unselect_cards(self, carrousel_card: CarrouselCard):
        for card in self.carrousel_cards:
            if card != carrousel_card:
                card.unselect()

    def validate_card(self):
        for card in self.carrousel_cards:
            if card.coffee_type == self.current_coffee_type:
                card.validate_card()

    def on_card_validation(self, coffee_type: CoffeeType):
        for card in self.carrousel_cards:
            card.active = False
        self.main_window.selections.append(Selection(coffee_type, 0))
        if coffee_type.sweet:
            self.main_window.set_scene(Scenes.SUGAR)
        else:
            self.main_window.selections[-1].sugar = 0
            self.main_window.set_scene(Scenes.RECAP)

    def auto_scroll(self):
        scroll_bar = self.scrollArea.horizontalScrollBar()
        scroll_bar.setValue(
            scroll_bar.value() + self.scroll_direction * 5
        )  # Adjust step size as needed

    def check_scroll(self):
        max_value = self.scrollArea.horizontalScrollBar().maximum()
        current_value = self.scrollArea.horizontalScrollBar().value()

        if current_value == max_value:  # Scrolled to the right end
            self.move_first_to_end()
        elif current_value == 0:  # Scrolled to the left end
            self.move_last_to_start()

    def move_first_to_end(self):
        first_item = self.carrousel_cards.pop(0)
        self.layout.removeWidget(first_item)
        self.layout.addWidget(first_item)
        self.carrousel_cards.append(first_item)
        self.scrollArea.horizontalScrollBar().setValue(
            self.scrollArea.horizontalScrollBar().value() - first_item.width()
        )

    def move_last_to_start(self):
        last_item = self.carrousel_cards.pop(-1)
        self.layout.removeWidget(last_item)
        self.layout.insertWidget(0, last_item)
        self.carrousel_cards.insert(0, last_item)
        self.scrollArea.horizontalScrollBar().setValue(
            self.scrollArea.horizontalScrollBar().value() + last_item.width()
        )

    def hideEvent(self, event):
        self.current_card = None

    def move_cards_left(self):
        # Move the scroll area view 4 cards to the left
        self.main_window.swipe_sound.play()
        self.main_window.idle_timer.start(15000)
        self.adjust_scroll(-4)

    def move_cards_right(self):
        # Move the scroll area view 4 cards to the right
        self.main_window.swipe.sound.play()
        self.main_window.idle_timer.start(15000)
        self.adjust_scroll(4)

    def adjust_scroll(self, num_cards):
        # Calculate the width of a single card
        if self.carrousel_cards:
            card_width = self.carrousel_cards[0].width()

            # Get the current scroll position
            scroll_bar = self.scrollArea.horizontalScrollBar()
            current_value = int(scroll_bar.value() / card_width)

            # Calculate the new scroll position
            new_value = (current_value + num_cards)% 8  * card_width

            # Set the new scroll position
            scroll_bar.setValue(new_value)
