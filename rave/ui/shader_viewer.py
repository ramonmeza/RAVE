import moderngl

from moderngl_window.geometry import quad_fs
from typing import Dict, List


DEFAULT_VERTEX_SHADER_SOURCE_CODE: str = """#version 330 core

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 uv0;

void main()
{
    gl_Position = vec4(in_position, 1);
    uv0 = in_texcoord_0;
}
"""

BUFFER_SIZE: int = 1024


class ShaderViewer:
    program: moderngl.Program
    VAO: moderngl.VertexArray
    VBO: moderngl.Buffer
    audio_rms: float
    audio_fft: List[float]

    def __init__(self) -> None:
        self.program = None
        self.VAO = None
        self.VBO = None

    def compile(
        self, context: moderngl.Context, fragment_shader_source_code: str
    ) -> None:
        self.program = context.program(
            vertex_shader=DEFAULT_VERTEX_SHADER_SOURCE_CODE,
            fragment_shader=fragment_shader_source_code,
        )

        self.VAO = quad_fs()
        self.update_uniforms()

    def update_resolution(self, width: float, height: float) -> None:
        if self.program is not None:
            if "u_resolution" in self.program:
                self.program["u_resolution"] = width, height

    def update_uniforms(
        self,
        u_time: float = 0.0,
        u_frametime: float = 0.0,
        u_audio_rms: float = 0.0,
        u_audio_fft: List[float] = [],
    ) -> None:
        if self.program is not None:
            if "u_time" in self.program:
                self.program["u_time"] = u_time

            if "u_frametime" in self.program:
                self.program["u_frametime"] = u_frametime

            if "u_audio_rms" in self.program:
                self.program["u_audio_rms"] = u_audio_rms

            if "u_audio_fft" in self.program and len(u_audio_fft) >= int(
                BUFFER_SIZE / 2
            ):
                self.program["u_audio_fft"].write(
                    u_audio_fft[: int(BUFFER_SIZE / 2)].astype("f4")
                )

    def render(
        self, time: float, frametime: float, rms: float, fft: List[float]
    ) -> None:
        self.update_uniforms(time, frametime, rms, fft)
        if self.VAO is not None:
            self.VAO.render(self.program)
