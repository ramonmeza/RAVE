import imgui
import moderngl

from moderngl_window import WindowConfig
from moderngl_window.integrations.imgui import ModernglWindowRenderer

from rave.database.database import Database
from rave.ui.editor_window import EditorWindow
from rave.ui.login_window import LoginWindow


class App(WindowConfig):
    _imgui_renderer: ModernglWindowRenderer

    _database: Database
    _login_window: LoginWindow
    _editor_window: EditorWindow
    _user_id: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # imgui integration
        imgui.create_context()
        self._imgui_renderer = ModernglWindowRenderer(self.wnd)

        # connect to database
        self._database = Database()
        self._database.open("rave.db")
        self._user_id = -1

        # window inits
        self._login_window = LoginWindow(
            self.login_submit_callback, self.login_register_callback
        )
        self._editor_window = EditorWindow()
        self._editor_window.open()

    # callbacks
    def login_submit_callback(self, email: str, password: str) -> None:
        self._user = self._database.login(email, password)

    def login_register_callback(self, email: str, password: str) -> None:
        pass

    # methods
    def render(self, time: float, frametime: float) -> None:
        self.render_ui()

    def render_ui(self) -> None:
        imgui.new_frame()

        self._editor_window.render()
        self._login_window.render()

        imgui.render()
        self._imgui_renderer.render(imgui.get_draw_data())
        imgui.end_frame()

    # window events
    def resize(self, width: int, height: int):
        self.aspect_ratio = width / height
        imgui.get_io().display_size = width, height
        self._imgui_renderer.resize(width, height)
        super().resize(width, height)

    def key_event(self, key, action, modifiers) -> None:
        self._imgui_renderer.key_event(key, action, modifiers)
        super().key_event(key, action, modifiers)

    def mouse_position_event(self, x: int, y: int, dx: int, dy: int) -> None:
        self._imgui_renderer.mouse_position_event(x, y, dx, dy)
        super().mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x: int, y: int, dx: int, dy: int) -> None:
        self._imgui_renderer.mouse_drag_event(x, y, dx, dy)
        super().mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float) -> None:
        self._imgui_renderer.mouse_scroll_event(x_offset, y_offset)
        super().mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x: int, y: int, button: int) -> None:
        self._imgui_renderer.mouse_press_event(x, y, button)
        super().mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int) -> None:
        self._imgui_renderer.mouse_release_event(x, y, button)
        super().mouse_release_event(x, y, button)

    def unicode_char_entered(self, char: str) -> None:
        self._imgui_renderer.unicode_char_entered(char)
        super().unicode_char_entered(char)

    def close(self) -> None:
        self._database.close()
        super().close()
