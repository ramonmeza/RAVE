import imgui

from typing import Callable, List, Optional

from rave.ui.editor_tab import EditorTab
from rave.ui.audio_config_tab import AudioConfigTab
from rave.ui.scripting_editor_tab import ScriptingEditorTab
from rave.ui.window import Window


class EditorWindow(Window):
    editors_tabs: EditorTab

    def __init__(
        self,
        audio_drivers: List[str],
        default_driver_index: int,
        apply_btn_callback: Callable[[str], None],
    ) -> None:
        super().__init__("Editor")

        self.editors_tabs = [
            ScriptingEditorTab(),
            AudioConfigTab(audio_drivers, default_driver_index, apply_btn_callback),
        ]

    def draw(self) -> None:
        with imgui.begin_group():
            with imgui.begin_tab_bar("tab_bar") as tab_bar:
                if tab_bar.opened:
                    for tab in self.editors_tabs:
                        tab.render()
