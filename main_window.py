import sys
from enum import Enum

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import QSoundEffect


from config import IDLE_TIMER

from scenes.options import OptionsScene
from scenes.idle import IdleScene
from scenes.coffee_selection import CoffeeSelectionScene
from scenes.sugar_selection import SugarSelectionScene
from scenes.recap import RecapScene
from scenes.payment import PaymentScene
from scenes.preparation import PreparationScene

from components.scenes import Scenes
from components.selection import CoffeeType, Selection
from components.top_bar import TopBar
from components.assets import wood_bg, resource_path
from components.parameters import GlobalParameters, Parameter


class MouseGlobalEventFilter(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            self.window.mouseMoveEvent(event)
        return super().eventFilter(obj, event)


class MainWindow(QMainWindow):
    def __init__(self, debug: bool):
        self.debug = debug
        super().__init__()
        self.initializing = True
        self.init_global_parameters()
        self.init_scenes()
        self.init_timers()
        self.init_sounds()
        self.initUI()
        self.init_selections()
        self.show()
        self.setMouseTracking(True)  # Enable mouse tracking
        self.reset_cursor_position()

    def init_global_parameters(self):
        self.params = GlobalParameters.getInstance()
        self.params.addParameter(
            "carrousel_swipe", False, "Carrousel scroll / swipe"
        )  # Scroll by default
        self.params.addParameter("clickable_button", False, "Clickable cards")
        self.params.addParameter("movement_validation", False, "Movement validation")
        self.params.addParameter("cursor_hidden", False, "Cursor hidden")
        self.params.addParameter("debug", False, "Debug mode")
        self.on_idle = True

    def init_scenes(self):
        self.options_scene = OptionsScene(self.params)
        self.idle_scene = IdleScene()
        self.main_scene = QWidget()

        self.sub_stack = QStackedWidget()  # Initialize self.stack here
        self.coffee_selection_scene = CoffeeSelectionScene()
        self.sugar_selection_scene = SugarSelectionScene()
        self.recap_selection_scene = RecapScene()
        self.payment_scene = PaymentScene()
        self.preparation_scene = PreparationScene()

        self.scenes = [
            self.coffee_selection_scene,
            self.sugar_selection_scene,
            self.recap_selection_scene,
            self.payment_scene,
            self.preparation_scene,
        ]

        for scene in self.scenes:
            self.sub_stack.addWidget(scene)

        self.main_scene.layout = QVBoxLayout(self.main_scene)
        self.main_scene.layout.setContentsMargins(0, 0, 0, 0)
        self.main_scene.setStyleSheet("border: 0px;")

        self.top_bar_container = QWidget()
        self.top_bar_layout = QHBoxLayout(self.top_bar_container)

        # Logo on left top
        top_bar_height = QApplication.primaryScreen().geometry().height() * 0.15
        self.image_label = QLabel()
        pixmap = QPixmap(resource_path("assets/linled_logo.png"))
        scaled_pixmap = pixmap.scaledToHeight(top_bar_height, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.top_bar_layout.addWidget(self.image_label, 1)
        self.top_bar_layout.addSpacing(10)

        # Top bar with progress
        self.top_bar = TopBar(0)
        self.top_bar.setFixedHeight(top_bar_height + 58)
        self.top_bar_layout.addWidget(self.top_bar, 8)
        self.top_bar_layout.setContentsMargins(20, 0, 20, 0)

        self.main_scene.layout.addWidget(self.top_bar_container)
        self.main_scene.layout.addWidget(self.sub_stack)

        self.main_stack = QStackedWidget()
        self.main_stack.setContentsMargins(0, 0, 0, 0)
        self.main_stack.addWidget(self.options_scene)
        self.main_stack.addWidget(self.idle_scene)
        self.main_stack.addWidget(self.main_scene)

    def init_sounds(self):
        self.validation_sound = QSoundEffect()
        self.validation_sound.setSource(
            QUrl.fromLocalFile(resource_path("assets/sounds/click.wav"))
        )

        self.change_sound = QSoundEffect()
        self.change_sound.setSource(
            QUrl.fromLocalFile(resource_path("assets/sounds/card_change.wav"))
        )

    def initUI(self):
        # Set the size of the window
        screen = QApplication.primaryScreen()
        rect = screen.geometry()
        self.width = rect.width()
        self.height = rect.height()
        self.setGeometry(0, 0, self.width, self.height)

        # Make the window frameless and fullscreen
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.background = QPixmap(wood_bg)

        # Create a label and set its size to fill the window
        self.background_label = QLabel(self)
        self.font = QFont("Arial", 16)
        self.background_label.setGeometry(0, 0, 800, 600)
        self.background_label.setScaledContents(True)

        # Example: Switch to scene two
        self.sub_stack.setCurrentIndex(Scenes.COFFEE.value)
        self.sub_stack.setMouseTracking(True)
        self.main_stack.setCurrentIndex(2)
        # self.main_stack.setContentsMargins(100, 100, 100, 100)

        self.setContentsMargins(0, 0, 0, 0)
        self.sub_stack.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.main_stack)

    def init_timers(self):
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.onIdle)
        self.idle_timer.start(IDLE_TIMER)

    def init_selections(self):
        self.selections = []
        self.selections.append(Selection(CoffeeType.NONE, 0))
        
    def onIdle(self):
        self.on_idle = True
        self.main_stack.setCurrentIndex(1)

    def exitIdle(self):
        self.reset()
        self.on_idle = False
        self.main_stack.setCurrentIndex(2)

    def reset(self):
        self.selections = []
        self.set_scene(Scenes.COFFEE)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.on_idle:
            self.exitIdle()
        else:
            self.idle_timer.start(IDLE_TIMER)

    def keyPressEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key_O:
                if self.main_stack.currentIndex() != 0:
                    self.main_stack.setCurrentIndex(0)
                    self.idle_timer.stop()
                    if self.on_idle:
                        self.on_idle = False
                else:
                    self.idle_timer.start(IDLE_TIMER)
                    self.main_stack.setCurrentIndex(2)
                return

    def set_scene(self, scene: Scenes):
        self.top_bar.set_state(scene.value)
        QTimer.singleShot(1500, lambda: self.sub_stack.setCurrentIndex(scene.value))
        QTimer.singleShot(1500, lambda: self.idle_timer.start(IDLE_TIMER))
        if not self.initializing:
            QTimer.singleShot(1500, lambda: self.reset_cursor_position())
        else:
            self.initializing = False

    def reset_cursor_position(self):
        QCursor.setPos(self.width / 2, self.height / 2)

    def validate_selection(self):
        self.selections.append(self.current_selection)
        self.selections[-1] = CoffeeType.NONE
