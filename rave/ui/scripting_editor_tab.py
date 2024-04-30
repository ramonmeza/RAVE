import imgui

from rave.ui.editor_tab import EditorTab


class ScriptingEditorTab(EditorTab):
    def __init__(self) -> None:
        super().__init__("Scripting")

    def draw(self) -> None:
        imgui.text("Scripting")
