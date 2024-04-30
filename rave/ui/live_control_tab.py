import imgui
import pyaudiowpatch as pyaudio

from rave.ui.editor_tab import EditorTab
from typing import Callable, List, Optional


STREAM_ON_STARTUP: bool = False


class LiveControlTab(EditorTab):
    def __init__(self) -> None:
        super().__init__("Live Control")

    def draw(self) -> None:
        imgui.text("Live Control")
