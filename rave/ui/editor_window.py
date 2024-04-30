import imgui

from typing import Callable, List, Optional

from rave.ui.editor_tab import EditorTab
from rave.ui.audio_config_tab import AudioConfigTab
from rave.ui.live_control_tab import LiveControlTab
from rave.ui.scripting_editor_tab import ScriptingEditorTab
from rave.ui.window import Window


SCRIPTING_EDITOR_TAB_INDEX: int = 0
LIVE_CONTROL_TAB_INDEX: int = 1


class EditorWindow(Window):
    editors_tabs: EditorTab

    def __init__(
        self,
        audio_drivers: List[str],
        default_driver_index: int,
        apply_audio_btn_callback: Callable[[str], None],
        compile_shader_callback: Callable[[str], None],
    ) -> None:
        super().__init__("Editor")

        self.editors_tabs = [
            ScriptingEditorTab(compile_shader_callback),
            LiveControlTab(),
            AudioConfigTab(
                audio_drivers, default_driver_index, apply_audio_btn_callback
            ),
        ]

    def get_fragment_source_code(self) -> str:
        return self.editors_tabs[
            SCRIPTING_EDITOR_TAB_INDEX
        ]._fragment_shader_source_code

    def update_live_controls(self, program) -> None:
        self.editors_tabs[LIVE_CONTROL_TAB_INDEX].update_controls(program)

    def draw(self) -> None:
        with imgui.begin_group():
            with imgui.begin_tab_bar("tab_bar") as tab_bar:
                if tab_bar.opened:
                    for tab in self.editors_tabs:
                        tab.render()
