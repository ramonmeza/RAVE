import imgui

from rave.project import Project
from rave.tool_window import ToolWindow


class LiveControlWindow(ToolWindow):
    def __init__(self, opened: bool = False) -> None:
        super().__init__("Live Control", opened)

    def draw(self, project: Project, **kwargs) -> None:
        for u in project.uniform_fields:
            expanded, _ = imgui.collapsing_header(u.name)

            if expanded:
                imgui.push_item_width(120.0)
                changed, min_max = imgui.input_float2(
                    f"Min/Max##{u.name}",
                    u.min_value,
                    u.max_value,
                )
                imgui.pop_item_width()

                if changed:
                    u.min_value = min_max[0]
                    u.max_value = min_max[1]

                imgui.same_line()

                # @todo: make this not a huge if.elif statement, maybe?
                if u.fmt == "1f":
                    imgui.push_item_width(200.0)
                    _, u.value = imgui.slider_float(
                        f"Value##{u.name}", u.value, u.min_value, u.max_value
                    )
                    imgui.pop_item_width()
                elif u.fmt == "2f":
                    _, u.value = imgui.slider_float2(
                        f"Value##{u.name}",
                        u.value[0],
                        u.value[1],
                        u.min_value,
                        u.max_value,
                    )

            imgui.separator()
