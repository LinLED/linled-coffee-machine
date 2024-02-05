import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    # Check if we are running in a bundle (PyInstaller)
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:	
        # Determine the base path relative to this file's location
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


svg_file_path = resource_path("assets\contactless-icon.svg")
sound_path = resource_path("assets\sounds\click.click.wav")
wood_bg = resource_path("assets\wood_bg.jpg")
