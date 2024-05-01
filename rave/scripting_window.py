import imgui

from typing import Callable, Optional

from rave.project import Project
from rave.tool_window import ToolWindow


ScriptChangedCallback = Optional[Callable[[None], None]]


class ScriptingWindow(ToolWindow):
    script_changed_callback: ScriptChangedCallback

    def __init__(
        self, script_changed_callback: ScriptChangedCallback = None, opened: bool = True
    ) -> None:
        super().__init__("Scripting", opened)
        self.script_changed_callback = script_changed_callback

    def draw(self, project: Project, **kwargs) -> None:
        changed, project.fragment_shader_source_code = imgui.input_text_multiline(
            "GLSL Source Code",
            project.fragment_shader_source_code,
            flags=imgui.INPUT_TEXT_ALLOW_TAB_INPUT,
        )

        if changed and self.script_changed_callback is not None:
            self.script_changed_callback()
