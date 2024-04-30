import imgui
import moderngl

from rave.ui.editor_tab import EditorTab
from typing import List

MIN_VAL: float = -25.0
MAX_VAL: float = 25.0


class LiveControlTab(EditorTab):
    _uniforms: List[moderngl.Uniform]

    def __init__(self) -> None:
        super().__init__("Live Control")
        self._uniforms = []

    def update_controls(self, program: moderngl.Program) -> None:
        # save old values
        old_uniforms = {}
        for u in self._uniforms:
            old_uniforms[(u.name, u.fmt)] = u.value

        # clear 
        self._uniforms.clear()

        # set values
        for key in program:
            if not isinstance(key, moderngl.Uniform):
                if key in [
                    "in_position",
                    "in_texcoord_0",
                    "u_time",
                    "u_frametime",
                    "u_resolution",
                    "u_audio_rms",
                    "u_audio_fft",
                ]:
                    continue

                u = program[key]
                uk = (u.name, u.fmt)
                if uk in old_uniforms:
                    u.value = old_uniforms[uk]

                self._uniforms.append(u)

    def draw(self) -> None:
        with imgui.begin_group():
            for u in self._uniforms:
                # int
                if u.fmt == "1i":
                    _, u.value = imgui.slider_int(u.name, u.value, MIN_VAL, MAX_VAL)

                # float
                elif u.fmt == "1f":
                    # display float slider
                    _, u.value = imgui.slider_float(u.name, u.value, MIN_VAL, MAX_VAL)

                # vec2
                elif u.fmt == "2f":
                    _, u.value = imgui.slider_float2(
                        u.name, u.value[0], u.value[1], MIN_VAL, MAX_VAL
                    )

                # vec3
                elif u.fmt == "3f":
                    _, u.value = imgui.slider_float3(
                        u.name, u.value[0], u.value[1], u.value[2], MIN_VAL, MAX_VAL
                    )

                # vec4
                elif u.fmt == "4f":
                    _, u.value = imgui.slider_float4(
                        u.name, u.value[0], u.value[1], u.value[2], MIN_VAL, MAX_VAL
                    )
                else:
                    raise NotImplementedError
