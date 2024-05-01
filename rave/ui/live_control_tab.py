import imgui
import moderngl

from rave.ui.editor_tab import EditorTab
from typing import List, Tuple

MIN_VAL: float = -25.0
MAX_VAL: float = 25.0


class LiveControlTab(EditorTab):
    # _uniforms: List  # [uniform, (min, max)]
    _uniforms = 

    def __init__(self) -> None:
        super().__init__("Live Control")
        self._uniforms = []

    def update_controls(self, program: moderngl.Program) -> None:
        # save old values
        old_uniforms = {}
        for u, _ in self._uniforms:
            old_uniforms[(u.name, u.fmt)] = u.value

        # clear
        self._uniforms.clear()

        # set values
        for key in program:
            # ignore uniforms that we handle internally
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

            # get the user defined uniforms
            u = program[key]
            if isinstance(u, moderngl.Uniform):
                uk = (u.name, u.fmt)
                if uk in old_uniforms:
                    u.value = old_uniforms[uk]

                self._uniforms.append([u, (-1.0, 1.0)])

    def draw(self) -> None:
        with imgui.begin_group():
            for i in range(len(self._uniforms)):
                u = self._uniforms[i][0]
                min_max = self._uniforms[i][1]

                imgui.push_item_width(100)
                _, self._uniforms[i][1] = imgui.input_float2(
                    "Min/Max", self._uniforms[i][1][0], self._uniforms[i][1][1]
                )
                imgui.pop_item_width()

                imgui.same_line()

                # int
                if u.fmt == "1i":
                    _, u.value = imgui.slider_int(
                        u.name,
                        u.value,
                        self._uniforms[i][1][0],
                        self._uniforms[i][1][1],
                    )

                # float
                elif u.fmt == "1f":
                    # display float slider
                    _, u.value = imgui.slider_float(
                        u.name,
                        u.value,
                        self._uniforms[i][1][0],
                        self._uniforms[i][1][1],
                    )

                # vec2
                elif u.fmt == "2f":
                    _, u.value = imgui.slider_float2(
                        u.name,
                        u.value[0],
                        self._uniforms[i][1][0],
                        self._uniforms[i][1][1],
                    )

                # vec3
                elif u.fmt == "3f":
                    _, u.value = imgui.slider_float3(
                        u.name,
                        u.value[0],
                        u.value[1],
                        u.value[2],
                        self._uniforms[i][1][0],
                        self._uniforms[i][1][1],
                    )

                # vec4
                elif u.fmt == "4f":
                    _, u.value = imgui.slider_float4(
                        u.name,
                        u.value[0],
                        u.value[1],
                        u.value[2],
                        self._uniforms[i][1][0],
                        self._uniforms[i][1][1],
                    )
                else:
                    raise NotImplementedError
