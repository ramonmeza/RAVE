import webbrowser

from typing import Any, Optional

import imgui
import moderngl

from moderngl_window import WindowConfig
from moderngl_window.integrations.imgui import ModernglWindowRenderer

from rave.audio_source import AudioSource
from rave.database.database import Database
from rave.ui.about_window import AboutWindow
from rave.ui.editor_window import EditorWindow
from rave.ui.login_window import LoginWindow
from rave.ui.shader_viewer import ShaderViewer


class App(WindowConfig):
    _imgui_renderer: ModernglWindowRenderer

    _audio_source: AudioSource
    _database: Database
    _about_window: AboutWindow
    _login_window: LoginWindow
    _editor_window: EditorWindow
    _shader_viewer: ShaderViewer
    _user: Optional[Any]
    _show_popup: bool
    _popup_message: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # imgui integration
        imgui.create_context()
        self._imgui_renderer = ModernglWindowRenderer(self.wnd)

        self._audio_source = AudioSource()
        self._shader_viewer = ShaderViewer()

        # connect to database
        self._database = Database()
        self._database.open("rave.db")
        self._user = None

        # window inits
        self._login_window = LoginWindow(
            self.login_submit_callback, self.login_register_callback
        )
        self._editor_window = EditorWindow(
            self._audio_source.get_available_drivers(),
            self._audio_source.get_default_loopback_driver(),
            self.apply_audio_config_callback,
            self.compile_shader_callback,
        )
        self._about_window = AboutWindow()
        self._editor_window.open()

        self._show_popup = False
        self._popup_message = ""

    # callbacks
    def login_submit_callback(self, email: str, password: str) -> None:
        self._user = self._database.login(email, password)
        if self._user is None:
            self.popup("Failed to login")
        else:
            self._login_window.close()

    def login_register_callback(self, email: str, password: str) -> None:
        self._user = self._database.register_user(email, password)

        if self._user is None:
            self.popup("Failed to register")
        else:
            self._login_window.close()

    def logout(self) -> None:
        self._user = None

    def apply_audio_config_callback(self, audio_device_index: int) -> None:
        self._audio_source.start_stream(input_device_index=audio_device_index)

    def compile_shader_callback(self, fragment_shader_source_code: str) -> None:
        try:
            self._shader_viewer.compile(self.ctx, fragment_shader_source_code)
        except Exception as e:
            print(f"Shader compilation error: {e}")

    # methods
    def popup(self, message: str) -> None:
        self._show_popup = True
        self._popup_message = message

    def render(self, time: float, frametime: float) -> None:
        self._shader_viewer.render(
            time, frametime, self._audio_source.rms, self._audio_source.fft
        )
        self.render_ui()

    def render_ui(self) -> None:
        imgui.new_frame()

        with imgui.begin_main_menu_bar() as menu_bar:
            with imgui.begin_menu("File") as file_menu:
                if file_menu.opened:
                    imgui.menu_item("Exit", "Alt+F4")

            with imgui.begin_menu("Window") as window_menu:
                if window_menu.opened:
                    clicked, _ = imgui.menu_item("Toggle Fullscreen", "F11")
                    if clicked:
                        self.wnd.fullscreen = not self.wnd.fullscreen

            with imgui.begin_menu("User") as user_menu:
                if user_menu.opened:
                    if self._user is None:
                        clicked, _ = imgui.menu_item("Login")
                        if clicked:
                            self._login_window.open()
                    else:
                        imgui.menu_item(self._user[1], enabled=False)
                        clicked, _ = imgui.menu_item("Log Out")
                        if clicked:
                            self.logout()

            with imgui.begin_menu("Help") as help_menu:
                if help_menu.opened:
                    clicked, _ = imgui.menu_item("Documentation")
                    if clicked:
                        webbrowser.open("https://github.com/ramonmeza/RAVE")

                    clicked, _ = imgui.menu_item("About RAVE")
                    if clicked:
                        self._about_window.open()

        self._editor_window.render()
        self._login_window.render()
        self._about_window.render()

        # popup
        if self._show_popup:
            imgui.open_popup("popup")
            self._show_popup = False

        with imgui.begin_popup("popup") as popup:
            if popup.opened:
                imgui.text_colored(self._popup_message, 1.0, 0.0, 0.0)

        imgui.render()
        self._imgui_renderer.render(imgui.get_draw_data())
        imgui.end_frame()

    # window events
    def resize(self, width: int, height: int):
        self.aspect_ratio = width / height
        imgui.get_io().display_size = width, height
        self._shader_viewer.update_resolution(width, height)
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
        self._audio_source.close()
        self._database.close()
        super().close()
