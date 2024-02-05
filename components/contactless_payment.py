from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSvg import *
from PySide6.QtMultimedia import *

from config import PAYMENT_TIMER

from components.assets import svg_file_path, resource_path


class ContactlessPayment(QWidget):
    animation_finished = Signal()  # Signal to be emitted when animation finishes

    def __init__(self, parent=None):
        super().__init__(parent)
        self._border_progress = 0.0
        self.sound_path = "assets/sounds/validate.wav"
        self.initUI()
        self.setup_animation()
        self.setup_sound()
        self.setStyleSheet("border: 2px solid black;")

    def initUI(self):
        self.svgRenderer = QSvgRenderer(svg_file_path)  # Load the SVG file
        self.setFixedSize(150, 150)  # Set the size of the widget
        self.move_to_center()

    def setup_sound(self):
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(self.sound_path))

    def move_to_center(self):
        # Get widget dimensions
        widget_width = self.frameGeometry().width()
        widget_height = self.frameGeometry().height()

        # Check if the widget has a parent
        parent = self.parent()
        if parent is None:
            # Center on screen
            screen_geometry = QApplication.primaryScreen().geometry()
            x = (screen_geometry.width() - widget_width) // 2
            y = (screen_geometry.height() - widget_height) // 2
        else:
            # Center in the parent
            parent_geometry = parent.frameGeometry()
            x = (parent_geometry.width() - widget_width) // 2
            y = (parent_geometry.height() - widget_height) // 2

        self.move(500, 500)

    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"borderProgress")
        self.animation.setDuration(PAYMENT_TIMER)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.finished.connect(self.onAnimationFinished)

    def onAnimationFinished(self):
        self.sound_effect.play()
        self.animation_finished.emit()  # Emit the signal when animation is finished

    def showEvent(self, event):
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensions du widget
        widget_width = self.width()
        widget_height = self.height()

        # Taille de l'image et du cercle
        image_size = 120  # ou toute autre taille appropriée pour votre image SVG

        # Calcul du rectangle central pour le SVG
        rect_svg = QRectF(
            (widget_width - image_size) / 2,
            (widget_height - image_size) / 2,
            image_size,
            image_size,
        )

        # Ajuster le QRectF pour l'arc
        arc_padding = (
            10  # L'espace entre l'arc et l'image SVG, ajustez selon vos besoins
        )
        arc_size = image_size + 2 * arc_padding
        rect_arc = QRectF(
            (widget_width - arc_size) / 2,
            (widget_height - arc_size) / 2,
            arc_size,
            arc_size,
        )

        # Dessiner l'image SVG
        self.svgRenderer.render(painter, rect_svg)

        # Dessiner le cercle
        painter.setBrush(QBrush(QColor(219, 193, 172, 0)))
        painter.drawEllipse(rect_arc)

        # Dessiner la bordure avec la progression de l'animation
        pen = QPen(QColor(219, 193, 172), 3)
        painter.setPen(pen)
        painter.drawArc(rect_arc, 90 * 16, -360 * 16 * self._border_progress)

    def getBorderProgress(self):
        return self._border_progress

    def setBorderProgress(self, value):
        self._border_progress = value
        self.update()  # Trigger a repaint

    borderProgress = Property(float, getBorderProgress, setBorderProgress)
