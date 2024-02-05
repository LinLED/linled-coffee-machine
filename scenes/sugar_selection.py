from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import QSoundEffect

from config import *

from components.assets import resource_path
from components.scenes import Scenes
from components.top_bar import TopBar
from components.utils import findMainWindow
from components.validate_bottom import ValidateBottomZone
from components.style import COFFEE_COLOR

MAX_SUGAR = 5
TITLE_SPACING = 20


class Block(QWidget):
    hover_signal = Signal(int)

    def __init__(self, block_height):
        super().__init__()
        self.block_height = block_height
        self.setFixedWidth(20)
        self.setMinimumHeight(self.block_height)
        self.setMaximumHeight(20)
        self.setStyleSheet(f"border: 0px; background-color:{COFFEE_COLOR[3]};")
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def enterEvent(self, event):
        self.color = self.hover_color
        self.update()

    def leaveEvent(self, event):
        self.color = self.default_color
        self.update()

    def hideEvent(self, event):
        pass


class NoSugarBox(QWidget):
    validate_sugar_signal = Signal(int)

    def __init__(self, sugar_scene):
        super().__init__()
        self.sugar_scene = sugar_scene
        self._text = "No Sugar"
        self.loadAssets()
        self.init_font()
        self.initUI()

    def init_font(self):
        self.font_db = QFontDatabase()
        self.font_id = self.font_db.addApplicationFont(
            resource_path("assets/fonts/arlrdbd.ttf")
        )
        if self.font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        else:
            print("Failed to load and register the custom font.")

    def loadAssets(self):
        self.image_label = QLabel(self)
        self.image_path = resource_path("assets/no_sugar.png")
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Scale image to fit the label size

    def initUI(self):
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.addSpacing(TITLE_SPACING)

        self.label = QLabel("No sugar")
        self.label.setFont(QFont(self.font_family, 48))
        self.label.setStyleSheet(
            f"border: 2px; color: {COFFEE_COLOR[1]}; background-color: transparent;"
        )
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.container_layout.addWidget(self.label, 1, Qt.AlignTop | Qt.AlignHCenter)
        self.font = QFont("Arial", 32)

        max_width = 150  # Replace with your desired maximum width
        max_height = 150  # Replace with your desired maximum height
        self.image_label.setMaximumSize(max_width, max_height)
        self.image_label.setStyleSheet("border: 0px; background-color: transparent;")

        self.container_layout.addWidget(
            self.image_label, 9, Qt.AlignCenter | Qt.AlignHCenter
        )
        self.margins = 20

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.container)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)

    def enterEvent(self, event):
        self.parent().unselect_widgets()
        self.select(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def select(self, event):
        self.main_window.change_sound.play()
        self.sugar_scene.sugar_value = 0
        self.container.setStyleSheet(
            f"border: 2px solid {COFFEE_COLOR[1]}; background-color: rgba(150, 114, 89, 220); border-radius: 5px;"
        )
        self.label.setStyleSheet(
            f"color: {COFFEE_COLOR[0]}; border: 0px; background-color: transparent;"
        )

    def unselect(self):
        self.container.setStyleSheet(
            f"border: 2px solid {COFFEE_COLOR[4]}; background-color: rgba(150, 114, 89, 128);border-radius: 5px;"
        )
        self.label.setStyleSheet(
            f"color: {COFFEE_COLOR[1]};border: 0px; background-color: transparent;"
        )

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def validate_card(self):
        self.main_window.validation_sound.play()
        self.validate_sugar_signal.emit(0)


class SugarBarBox(QWidget):
    validate_sugar_signal = Signal(int)

    def __init__(self, sugarScene):
        super().__init__()
        self.sugar_level = 3
        self.sugar_scene = sugarScene
        self.setMouseTracking(True)
        self.init_font()
        self.initUI()

    def init_font(self):
        self.font_db = QFontDatabase()
        self.font_id = self.font_db.addApplicationFont(
            resource_path("assets/fonts/arlrdbd.ttf")
        )
        if self.font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        else:
            print("Failed to load and register the custom font.")

    def initUI(self):
        self.container = QWidget()
        self.container.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.addSpacing(TITLE_SPACING)

        self.label = QLabel("Add some sugar ?")
        self.label.setFont(QFont(self.font_family, 48))
        self.label.setStyleSheet(
            f"border: 2px; color: {COFFEE_COLOR[1]}; background-color: transparent;"
        )
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.label.setContentsMargins(0, 0, 0, 0)

        self.container_layout.addWidget(self.label, 0, Qt.AlignTop | Qt.AlignHCenter)

        self.blocks_layout = QHBoxLayout()
        self.blocks = []

        for i in range(5):
            block_height = 50 + i * 75  # Increment height for each block
            block_container = QVBoxLayout()
            block = Block(block_height)
            block_container.addWidget(block, 0, Qt.AlignCenter)

            block_widget = QWidget()
            block_widget.setLayout(block_container)
            block_widget.setStyleSheet(
                f"border: 0px; background-color: {COFFEE_COLOR[3]};"
            )
            block_widget.setMaximumHeight(block_height)
            self.blocks_layout.addWidget(block_widget, 0, Qt.AlignBottom)
            self.blocks.append(block_widget)

        self.container_layout.addLayout(self.blocks_layout)
        self.container.setMinimumHeight(400)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.container)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)

    def enterEvent(self, event):
        self.parent().unselect_widgets()
        self.select(event)

    def leaveEvent(self, event):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def select(self, event):
        self.main_window.change_sound.play()
        self.container.setStyleSheet(
            f"border: 2px solid {COFFEE_COLOR[1]}; background-color: rgba(150, 114, 89, 220); border-radius: 5px;"
        )
        self.label.setStyleSheet(
            f"color: {COFFEE_COLOR[0]}; border: 0px; background-color: transparent;"
        )

    def unselect(self):
        self.container.setStyleSheet(
            f"border: 2px solid {COFFEE_COLOR[4]}; background-color: rgba(150, 114, 89, 128); border-radius: 5px;"
        )
        self.label.setStyleSheet(
          f"color: {COFFEE_COLOR[1]}; border: 0px; background-color: transparent;"
          )

    def hideEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        mouse_x = event.globalPosition().x()
        x = self.x()  # X position of the widget's top-left corner
        width = self.width()  # Width of the widget
        step = width / MAX_SUGAR
        min_x = x
        max_x = x + width

        if min_x <= mouse_x < min_x + step:
            sugar_value = 0
        elif min_x + step <= mouse_x < min_x + 2 * step:
            sugar_value = 1
        elif min_x + 2 * step <= mouse_x < min_x + 3 * step:
            sugar_value = 2
        elif min_x + 3 * step <= mouse_x < min_x + 4 * step:
            sugar_value = 3
        elif min_x + 4 * step <= mouse_x <= min_x + 5 * step:
            sugar_value = 4

        self.sugar_level = sugar_value
        self.sugar_scene.sugar_value = sugar_value + 1
        self.colorBlocks(self.sugar_level)

    def colorBlocks(self, sugar_value):
        for block in self.blocks:
            if self.blocks.index(block) <= sugar_value:
                block.setStyleSheet(f"background-color: {COFFEE_COLOR[1]};")
            else:
                block.setStyleSheet(f"background-color: {COFFEE_COLOR[3]};")
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def validate_card(self):
        self.main_window.validation_sound.play()
        self.validate_sugar_signal.emit(self.sugar_level)


class SugarSelectionScene(QWidget):
    def __init__(self):
        super().__init__()
        self.lastMousePosition = QPoint()
        self.elapsedTimer = QElapsedTimer()
        self.validate_bottom_zone = None
        self.sugar_value = 0
        self.initUI()

    def initUI(self):
        self.no_sugar_box = NoSugarBox(self)
        self.no_sugar_box.setStyleSheet("background-color: rgba(150, 114, 89, 64)")
        self.no_sugar_box.setContentsMargins(0, 0, 0, 0)
        self.no_sugar_box.validate_sugar_signal.connect(self.validate_sugar)
        self.no_sugar_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.sugar_bar_box = SugarBarBox(self)
        self.sugar_bar_box.setStyleSheet("background-color: rgba(150, 114, 89, 64)")
        self.sugar_bar_box.setContentsMargins(0, 0, 0, 0)
        self.sugar_bar_box.validate_sugar_signal.connect(self.validate_sugar)
        self.sugar_bar_box.setMinimumHeight(570)

        self.under_layout = QHBoxLayout()
        self.under_layout.setContentsMargins(0, 0, 0, 0)
        self.under_layout.addWidget(self.no_sugar_box, 2)
        self.under_layout.addWidget(self.sugar_bar_box, 5)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.under_layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.add_bottom_validation()

    def showEvent(self, event):
        self.main_window = findMainWindow(self)

    def add_bottom_validation(self):
        self.validate_bottom_zone = ValidateBottomZone()
        self.validate_bottom_zone.setContentsMargins(0, 0, 0, 0)
        self.validate_bottom_zone.validate_signal.connect(self.validate_card)
        self.layout.addWidget(self.validate_bottom_zone, alignment=Qt.AlignBottom)

    def remove_bottom_validation(self):
        if self.validate_bottom_zone is not None:
            self.layout.removeWidget(self.validate_bottom_zone)
            self.validate_bottom_zone.deleteLater()
            self.validate_bottom_zone = None

    def validate_card(self):
        self.main_window.validation_sound.play()  # Play the sound
        self.validate_sugar()

    def validate_sugar(self):
        self.setMouseTracking(False)
        self.main_window.selections[-1].sugar = self.sugar_value
        self.main_window.set_scene(Scenes.RECAP)

    def unselect_widgets(self):
        self.no_sugar_box.unselect()
        self.sugar_bar_box.unselect()
        # self.full_sugar_box.unselect()
