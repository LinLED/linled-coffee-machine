from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from components.scenes import Scenes
from components.loading import ProgressionBar
from components.utils import findMainWindow
from components.assets import resource_path

class FadeInText(QWidget):
    fade_out_finished = Signal()  # Step 1: Add a new signal

    def __init__(self, text: str):
        super().__init__()
        self.init_font()
        self.init_ui(text)
        self.setup_animations()
        self.fade_out_animations_completed = (
            0  # Counter for completed fade-out animations
        )

    def init_font(self):
        self.font_db = QFontDatabase()
        self.font_id = self.font_db.addApplicationFont(
            resource_path("assets/fonts/arlrdbd.ttf")
        )
        if self.font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        else:
            print("Failed to load and register the custom font.")

    def init_ui(self, text: str):
        self.label = QLabel(text, alignment=Qt.AlignCenter)
        self.label.setStyleSheet("color: #dbc1ac;")
        self.font = QFont(self.font_family, 48)
        self.label.setFont(self.font)
        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)

        # Ajouter le widget de GIF ici
        self.gif_label = QLabel(self)
        self.movie = QMovie(resource_path("assets/cup.gif"))
        self.gif_label.setMovie(self.movie)
        self.layout.addWidget(self.gif_label, 0, Qt.AlignCenter)  # Ajouter le QLabel à la disposition
        self.movie.start()  # Commencer à jouer le GIF

    def setup_animations(self):
        """Set up the fade-in and fade-out animations."""
        # Fade-in animation
        self.fade_in_opacity_animation = QPropertyAnimation(
            self.opacity_effect, b"opacity"
        )
        self.fade_in_opacity_animation.setDuration(1000)
        self.fade_in_opacity_animation.setStartValue(0.0)
        self.fade_in_opacity_animation.setEndValue(1.0)

        self.fade_in_move_animation = QPropertyAnimation(self.label, b"pos")
        self.fade_in_move_animation.setDuration(1000)
        self.fade_in_move_animation.setStartValue(QPoint(0, 30))
        self.fade_in_move_animation.setEndValue(QPoint(0, 0))
        self.fade_in_move_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Fade-out animation
        self.fade_out_opacity_animation = QPropertyAnimation(
            self.opacity_effect, b"opacity"
        )
        self.fade_out_opacity_animation.setDuration(1000)
        self.fade_out_opacity_animation.setStartValue(1.0)
        self.fade_out_opacity_animation.setEndValue(0.0)

        self.fade_out_move_animation = QPropertyAnimation(self.label, b"pos")
        self.fade_out_move_animation.setDuration(1000)
        self.fade_out_move_animation.setStartValue(QPoint(0, 0))
        self.fade_out_move_animation.setEndValue(QPoint(0, 30))
        self.fade_out_move_animation.setEasingCurve(QEasingCurve.InQuad)
        self.fade_out_opacity_animation.finished.connect(self.check_fade_out_finished)
        self.fade_out_move_animation.finished.connect(self.check_fade_out_finished)

    def fade_in(self):
        """Start the fade-in animation."""
        self.fade_in_opacity_animation.start()
        self.fade_in_move_animation.start()

    def fade_out(self):
        """Start the fade-out animation."""
        self.fade_out_opacity_animation.start()
        self.fade_out_move_animation.start()

    def check_fade_out_finished(self):
        """Check if both fade-out animations have finished."""
        self.fade_out_animations_completed += 1
        if self.fade_out_animations_completed == 2:
            self.fade_out_finished.emit()  # Emit the signal when both animations are finished
            self.fade_out_animations_completed = 0  # Reset the counter


class PreparationScene(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.counter = 0

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.preparation_text = FadeInText("Preparing your order, please wait...")
        self.layout.addWidget(self.preparation_text)
        self.preparation_text.fade_out_finished.connect(self.preparation_finished)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)
        self.main_window.top_bar.set_state(5, 5000)
        self.preparation_text.fade_in()
        QTimer.singleShot(5000, self.preparation_text.fade_out)

    def preparation_finished(self):
        if self.counter == 0:
            self.preparation_text.label.setText("Here is your drink, enjoy!")
            self.preparation_text.fade_in()
            self.main_window
            QTimer.singleShot(3000, self.preparation_text.fade_out)
            self.counter += 1
        else:
            self.main_window.selections.clear()
            self.main_window.set_scene(Scenes.COFFEE)
