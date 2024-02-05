from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy
import sys


class MaxHeightWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setStyleSheet("background-color: red;")


class FixedSizeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 100)
        self.setStyleSheet("background-color: blue;")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        expanding_widget = MaxHeightWidget()
        layout.addWidget(expanding_widget)

        fixed_widget = FixedSizeWidget()
        layout.addWidget(fixed_widget)

        self.setLayout(layout)


# Example usage
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
