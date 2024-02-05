import sys
import argparse

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Assuming main_window.py is in the same directory
from main_window import MainWindow, MouseGlobalEventFilter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the application.")
    parser.add_argument("--debug", default=False, action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    app = QApplication(sys.argv)

    debug_mode = args.debug
    main_window = MainWindow(debug=debug_mode)

    filter = MouseGlobalEventFilter(main_window)

    app.installEventFilter(filter)

    main_window.show()
    sys.exit(app.exec())
