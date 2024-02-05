from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from components.assets import resource_path
from components.contactless_payment import ContactlessPayment
from components.scenes import Scenes
from components.style import COFFEE_COLOR
from components.utils import findMainWindow


class PaymentScene(QWidget):
    def __init__(self):
        super().__init__()
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
        self.main_layout = QVBoxLayout(self)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)

        # Titre
        self.text = QLabel("Proceed to payment...")
        self.font = QFont(self.font_family, 48)
        self.text.setFont(self.font)
        self.text.setStyleSheet(f"color: {COFFEE_COLOR[0]}; border: 0px;")
        self.container_layout.addWidget(self.text, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.container_layout.addSpacing(80)  # Ajustez cette valeur selon vos besoins

        # PNG
        self.image_label = QLabel()
        pixmap = QPixmap(resource_path("assets/cb.png"))
        scaled_pixmap = pixmap.scaled(
            pixmap.size() * 0.3, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # Centrer l'image si nécessaire
        self.container_layout.addWidget(self.image_label)
        self.container_layout.addSpacing(50)  # Ajustez cette valeur selon vos besoins

        # ContactlessPayment
        self.contactless_payment = ContactlessPayment(self)
        self.contactless_payment.animation_finished.connect(self.validatePayment)
        self.container_layout.addWidget(self.contactless_payment, 0, Qt.AlignCenter)

        # Ajouter un espace extensible pour pousser tout vers le haut
        self.container_layout.addStretch()

        self.main_layout.addWidget(self.container)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)

    def validatePayment(self):
        self.main_window = findMainWindow(self)
        self.main_window.set_scene(Scenes.PREPARATION)
