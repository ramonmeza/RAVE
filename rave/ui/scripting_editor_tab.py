import imgui

from rave.ui.editor_tab import EditorTab
from typing import Callable, Optional


BUFFER_SIZE: int = 1024
COMPILE_ON_STARTUP: bool = True


class ScriptingEditorTab(EditorTab):
    _compile_callback: Optional[Callable[[str], None]]
    _fragment_shader_source_code: str

    def __init__(
        self, compile_callback: Optional[Callable[[str], None]] = None
    ) -> None:
        super().__init__("Scripting")

        self._compile_callback = compile_callback
        self._fragment_shader_source_code = (
            """#version 330 core

uniform float u_resolution;
uniform float u_time;
uniform float u_frametime;
uniform float u_audio_rms;
"""
            + f"""uniform float u_audio_fft[{int(BUFFER_SIZE / 2)}];"""
            + """

out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}"""
        )

        if COMPILE_ON_STARTUP and self._compile_callback is not None:
            self._compile_callback(self._fragment_shader_source_code)

    def draw(self) -> None:
        with imgui.begin_group():
            imgui.button("Load")
            imgui.same_line()
            imgui.button("Save")

        changed, self._fragment_shader_source_code = imgui.input_text_multiline(
            "Fragment Shader Source Code (GLSL)",
            self._fragment_shader_source_code,
            flags=imgui.INPUT_TEXT_ALLOW_TAB_INPUT,
        )

        if changed and self._compile_callback is not None:
            self._compile_callback(self._fragment_shader_source_code)
