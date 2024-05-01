import moderngl

from moderngl_window.geometry import quad_fs
from typing import List, Optional

from rave.project import Project


class ShaderViewer:
    program: Optional[moderngl.Program]
    VAO: Optional[moderngl.VertexArray]

    def __init__(self) -> None:
        self.program = None
        self.VAO = quad_fs()

    def compile(
        self, context: moderngl.Context, project: Project
    ) -> List[moderngl.Uniform]:
        try:
            self.program = context.program(
                vertex_shader=project.vertex_shader_source_code,
                fragment_shader=project.fragment_shader_source_code,
            )

            return self.get_uniforms()
        except Exception as e:
            print(f"Shader compilation error: {e}")
            self.program = None
            return None

    def get_uniforms(self) -> List[moderngl.Uniform]:
        if self.program is None:
            return []

        uniform_list: List[moderngl.Uniform] = []

        for key in self.program:
            u = self.program[key]
            if isinstance(u, moderngl.Uniform):
                uniform_list.append(u)

        return uniform_list

    def render(self, time: float, frametime: float) -> None:
        if self.program is not None:
            self.VAO.render(self.program)
