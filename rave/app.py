import imgui
import moderngl

from moderngl_window import WindowConfig
from moderngl_window.integrations.imgui import ModernglWindowRenderer


class App(WindowConfig):
    _imgui_renderer: ModernglWindowRenderer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        imgui.create_context()
        self._imgui_renderer = ModernglWindowRenderer(self.wnd)

    def render(self, time: float, frametime: float) -> None:
        self.render_ui()

    def render_ui(self) -> None:
        imgui.new_frame()
        imgui.render()
        self._imgui_renderer.render(imgui.get_draw_data())
        imgui.end_frame()
