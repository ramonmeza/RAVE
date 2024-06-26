import imgui

from rave.project import Project
from rave.tool_window import ToolWindow


class ProjectOverviewWindow(ToolWindow):
    def __init__(self, opened: bool = True) -> None:
        super().__init__("Project Overview", opened)

    def draw(self, project: Project, **kwargs) -> None:
        _, project.name = imgui.input_text("Name", project.name)
        _, project.author = imgui.input_text("Author", project.author)
        _, project.description = imgui.input_text("Description", project.description)

        expanded, _ = imgui.collapsing_header("Uniforms")
        if expanded:
            for u in project.uniform_fields:
                expanded, _ = imgui.collapsing_header(u.name)
                if expanded:
                    imgui.input_text("Format", u.fmt, flags=imgui.INPUT_TEXT_READ_ONLY)
                    imgui.input_text(
                        "Value", str(u.value), flags=imgui.INPUT_TEXT_READ_ONLY
                    )
                    imgui.input_float2(
                        "Min/Max",
                        u.min_value,
                        u.max_value,
                        flags=imgui.INPUT_TEXT_READ_ONLY,
                    )

        expanded, _ = imgui.collapsing_header("Shader Source Code")
        if expanded:
            expanded, _ = imgui.collapsing_header("Vertex Shader Source Code")
            if expanded:
                imgui.input_text_multiline(
                    "GLSL Source Code##vertexshader",
                    project.vertex_shader_source_code,
                    flags=imgui.INPUT_TEXT_READ_ONLY,
                )

            expanded, _ = imgui.collapsing_header("Fragment Shader Source Code")
            if expanded:
                imgui.input_text_multiline(
                    "GLSL Source Code##fragmentshader",
                    project.fragment_shader_source_code,
                    flags=imgui.INPUT_TEXT_READ_ONLY,
                )
