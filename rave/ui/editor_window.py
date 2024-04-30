import imgui

from typing import Callable, Optional

from rave.ui.editor_tab import EditorTab
from rave.ui.audio_config_tab import AudioConfigTab
from rave.ui.scripting_editor_tab import ScriptingEditorTab
from rave.ui.window import Window


class EditorWindow(Window):
    editors_tabs: EditorTab

    def __init__(self) -> None:
        super().__init__("Editor")

        self.editors_tabs = [ScriptingEditorTab(), AudioConfigTab()]

    def draw(self) -> None:
        with imgui.begin_group():
            with imgui.begin_tab_bar("tab_bar") as tab_bar:
                if tab_bar.opened:
                    for tab in self.editors_tabs:
                        tab.render()
