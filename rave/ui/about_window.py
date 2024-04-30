import imgui
import re

from rave.ui.window import Window
from typing import Callable, Optional


class AboutWindow(Window):
    def __init__(self) -> None:
        super().__init__("About", True)

    def draw(self) -> None:
        with imgui.begin_group():
            imgui.text("RAVE: Real-time Audio Visualization Editor")
            imgui.text("Version 0.1.0")
            imgui.text("Created and developed by CZR")
