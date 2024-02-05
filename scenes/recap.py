from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from config import BASIC_FONT

from components.assets import resource_path
from components.carrousel_card import Selection
from components.contactless_payment import ContactlessPayment
from components.my_widget import MyWidget
from components.scenes import Scenes
from components.style import COFFEE_COLOR
from components.utils import findMainWindow
from components.validate_bottom import ValidateBottomZone


class RecapCardComponent(QWidget):
    def __init__(self, selection: Selection):
        super().__init__()
        self.init_font()
        self.initUI(selection)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def init_font(self):
        self.font_db = QFontDatabase()
        self.font_id = self.font_db.addApplicationFont(
            resource_path("assets/fonts/arlrdbd.ttf")
        )
        if self.font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        else:
            print("Failed to load and register the custom font.")

    def initUI(self, selection: Selection):
        self.container = QWidget()
        self.layout = QHBoxLayout(self.container)
        self.container.setStyleSheet("border: 2px solid #634832;")

        self.coffee_name = QLabel(selection.coffee_type.label)
        self.coffee_name.setFont(QFont(self.font_family, 20))
        self.coffee_name.setStyleSheet(
            f"border: 0px; background-color: transparent; color: {COFFEE_COLOR[1]}"
        )
        self.layout.addWidget(self.coffee_name, 0, Qt.AlignLeft)

        if selection.coffee_type.sweet:
            self.sugar_level = QLabel(f"Sugar: {selection.sugar}")
            self.sugar_level.setFont(QFont(self.font_family, 20))
            self.sugar_level.setStyleSheet(
                f"border: 0px; background-color: transparent; color: {COFFEE_COLOR[1]}"
            )
            self.layout.addWidget(self.sugar_level, 0, Qt.AlignRight)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.container)


class RecapCardList(QWidget):
    def __init__(self, selections):
        super().__init__()
        self.initUI(selections)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def initUI(self, selections):
        self.main_layout = QVBoxLayout(self)
        for selection in selections:
            current_card_component = RecapCardComponent(selection)
            current_card_component.setStyleSheet("border: 2px solid black;")
            self.main_layout.addWidget(current_card_component, 0, Qt.AlignTop)
        self.main_layout.addStretch()


class RecapCard(QWidget):
    card_validation_signal = Signal()

    def __init__(self):
        super().__init__()
        self._text = "Récapitulatif"
        self.elapsedTimer = QElapsedTimer()
        self.quickMoveThreshold = 150  # Threshold for quick movement, adjust as needed
        self.init_font()
        self.initUI()
        self.set_default_style()

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
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.addSpacing(20)

        # Title
        self.text = QLabel("Your order")
        self.text.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.font = QFont(self.font_family, 48)
        self.text.setFont(self.font)
        self.container_layout.addWidget(self.text, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.recap_card_list = None
        self.price_label = None

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.container)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.set_default_style()

    def add_recap_widget(self):
        if self.recap_card_list is None:
            self.recap_card_list = RecapCardList(self.main_window.selections)
            self.container_layout.addWidget(self.recap_card_list)
            # self.price_label = QLabel(f"Prix total: {len(self.main_window.selections)}")
            # self.font = QFont("Arial", 22)
            # self.price_label.setFont(self.font)
            # self.container_layout.addWidget(self.price_label, 0, Qt.AlignCenter)

    def showEvent(self, event):
        self.main_window = findMainWindow(self)
        self.add_recap_widget()
        self.recap_card_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.recap_card_list:
            self.container_layout.removeWidget(self.recap_card_list)
            self.recap_card_list.deleteLater()
            self.recap_card_list = None

        if self.price_label:
            self.container_layout.removeWidget(self.price_label)
            self.price_label.deleteLater()
            self.price_label = None

    def enterEvent(self, event):
        self.parent().active = Scenes.PAYMENT
        super().enterEvent(event)
        self.select(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def select(self, event):
        self.main_window.change_sound.play()
        self.parent().unselectCards()

        self.parent().active = Scenes.PAYMENT
        super().enterEvent(event)
        self.set_selected_style()

    def unselect(self):
        self.set_default_style()

    def validate_card(self):
        self.set_validated_style()
        self.main_window.validation_sound.play()
        self.card_validation_signal.emit()

    def set_default_style(self):
        self.container.setStyleSheet(
            """
            border: 2px solid #967259;
            background-color: rgba(150, 114, 89, 128);
            border-radius: 5px;
            """
        )
        self.text.setStyleSheet(
            f"""
            color: {COFFEE_COLOR[1]};
            border: 0px; 
            background-color: transparent;
            """
        )

    def set_selected_style(self):
        self.container.setStyleSheet(
            """
            border: 2px solid #ece0d1;
            background-color: rgba(150, 114, 89, 220);
            border-radius: 5px;
            """
        )
        self.text.setStyleSheet(
            f"""
            color: {COFFEE_COLOR[0]};
            border: 0px; 
            background-color: transparent;
            """
        )

    def set_validated_style(self):
        self.container.setStyleSheet(
            """
            border: 2px solid #ece0d1;
            background-color: rgba(219,193,172, 128);
            border-radius: 5px;
            """
        )


class AddAnotherCard(QWidget):
    card_validation_signal = Signal()

    def __init__(self):
        super().__init__()
        self._text = "Add another drink"
        self.elapsedTimer = QElapsedTimer()
        self.quickMoveThreshold = 150  # Threshold for quick movement, adjust as needed
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
        self.text = QLabel(self._text)
        self.text.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.font = QFont(self.font_family, 48)
        self.text.setFont(self.font)

        # Création du QLabel pour l'image
        self.imageLabel = QLabel()
        pixmap = QPixmap(
            resource_path("assets/mugs.jpg")
        )  # Remplacez par le chemin de votre image
        max_width = 500  # Définissez la largeur maximale souhaitée pour l'image
        pixmap = pixmap.scaled(
            max_width, max_width, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )  # Redimensionnement de l'image
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)  # Centrez l'image, si nécessaire

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.addSpacing(20)
        self.container_layout.addWidget(self.text, 1, Qt.AlignTop | Qt.AlignHCenter)
        self.container_layout.addSpacing(20)
        self.container_layout.addWidget(
            self.imageLabel, 9, Qt.AlignTop | Qt.AlignHCenter
        )  # Ajout de l'image sous le texte
        self.container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.container)

        self.set_default_style()

    def validate_card(self):
        self.set_validated_style()
        self.main_window.validation_sound.play()
        self.card_validation_signal.emit()

    def showEvent(self, event):
        self.main_window = findMainWindow(self)

    def enterEvent(self, event):
        self.select(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self.main_window.params.clickable_button.state:
            self.validate_card()

    def select(self, event):
        self.main_window.change_sound.play()
        self.parent().unselectCards()
        self.parent().active = Scenes.COFFEE
        self.set_selected_style()

    def unselect(self):
        self.set_default_style()

    def leaveEvent(self, event):
        pass

    def set_default_style(self):
        self.container.setStyleSheet(
            """
            border: 2px solid #967259;
            background-color: rgba(150, 114, 89, 128);
            border-radius: 5px;
            """
        )
        self.text.setStyleSheet(
            f"""
            color: {COFFEE_COLOR[1]};
            border: 0px; 
            background-color: transparent;
            """
        )

    def set_selected_style(self):
        self.container.setStyleSheet(
            """
            border: 2px solid #ece0d1;
            background-color: rgba(150, 114, 89, 220);
            border-radius: 5px;
            """
        )
        self.text.setStyleSheet(
            f"""
            color: {COFFEE_COLOR[0]};
            border: 0px; 
            background-color: transparent;
            """
        )

    def set_validated_style(self):
        self.container.setStyleSheet(
            """
            border: 2px solid #ece0d1;
            background-color: rgba(219,193,172, 64);
            border-radius: 5px;
            """
        )


class RecapScene(QWidget):
    def __init__(self):
        super().__init__()
        self.validate_bottom_zone = None
        self.active = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.mid_layout = QHBoxLayout()
        self.mid_layout.setContentsMargins(0, 0, 0, 0)

        self.recap_card = RecapCard()
        self.recap_card.card_validation_signal.connect(self.validate_command)
        self.recap_card.setContentsMargins(0, 0, 0, 0)
        self.mid_layout.addWidget(self.recap_card)

        self.another_card = AddAnotherCard()
        self.another_card.card_validation_signal.connect(self.add_another_command)
        self.another_card.setMinimumHeight(570)
        self.another_card.setContentsMargins(0, 0, 0, 0)
        self.mid_layout.addWidget(self.another_card)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(self.mid_layout)

    def set_default_style(self):
        self.recap_card.setStyleSheet("border: 2px solid black;")
        self.another_card.setStyleSheet("border: 2px solid black;")

    def validate_command(self):
        self.main_window = findMainWindow(self)
        self.main_window.set_scene(Scenes.PAYMENT)

    def add_another_command(self):
        self.main_window.set_scene(Scenes.COFFEE)
        
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

    def unselectCards(self):
        self.another_card.unselect()
        self.recap_card.unselect()

    def activate(self, scene):
        if scene == Scenes.COFFEE:
            self.recap_card.unselect()
        elif scene == Scenes.PAYMENT:
            self.another_card.unselect()

    def validate_card(self):
        self.main_window.validation_sound.play()
        if self.active == Scenes.PAYMENT:
            self.validate_command()
        elif self.active == Scenes.COFFEE:
            self.add_another_command()
