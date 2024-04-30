import imgui

from rave.ui.editor_tab import EditorTab


class AudioConfigTab(EditorTab):
    def __init__(self) -> None:
        super().__init__("Audio Config")

    def draw(self) -> None:
        imgui.text("Audio Config")
