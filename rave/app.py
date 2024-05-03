import enum
import imgui
import tkinter as tk

import moderngl
import moderngl_window
from moderngl_window import WindowConfig
from moderngl_window.context.base.keys import KeyModifiers
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import List, Optional, Tuple

from rave.live_control_window import LiveControlWindow
from rave.project import Project, UniformField, load_project, save_project
from rave.project_overview_window import ProjectOverviewWindow
from rave.scripting_window import ScriptingWindow
from rave.shader_viewer import ShaderViewer
from rave.tool_window import ToolWindow


# type aliases
FileTypeSpecifier = List[Tuple[str, ...]]


# constants
EXPOSED_UNIFORMS: List[str] = ["rTime"]


# enums
class WindowType(enum.IntEnum):
    PROJECT_OVERVIEW = 0
    SCRIPTING = 1
    LIVE_CONTROL = 2


# classes
class App(WindowConfig):
    _imgui_renderer: ModernglWindowRenderer

    project: Project
    windows: List[ToolWindow]
    shader_viewer: ShaderViewer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.project = Project()
        self.windows = [
            ProjectOverviewWindow(),
            ScriptingWindow(script_changed_callback=self.script_changed_callback),
            LiveControlWindow(),
        ]
        self.shader_viewer = ShaderViewer(
            update_uniforms_callback=self.update_uniforms_callback
        )

        imgui.create_context()
        self._imgui_renderer = ModernglWindowRenderer(self.wnd)

        self.script_changed_callback()

    # properties
    @property
    def project_overview_window(self) -> ProjectOverviewWindow:
        return self.windows[WindowType.PROJECT_OVERVIEW]

    @property
    def scripting_window(self) -> ScriptingWindow:
        return self.windows[WindowType.SCRIPTING]

    # methods
    def open_filedialog(
        self, filetypes: FileTypeSpecifier = [("All Files", "*")]
    ) -> Optional[str]:
        root = tk.Tk()
        root.withdraw()
        path = askopenfilename(filetypes=filetypes)
        return path if path else None

    def save_filedialog(
        self, defaultextension: str, filetypes: FileTypeSpecifier = [("All Files", "*")]
    ) -> bool:
        root = tk.Tk()
        root.withdraw()
        path = asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=defaultextension,
            filetypes=filetypes,
        )
        return path if path else None

    # callbacks
    def load_project_callback(self) -> None:
        path = self.open_filedialog([("RAVE Project", "*.raveproj")])
        if path is not None:
            self.project = load_project(path)
            if self.project is None:
                print("Failed to load project, using default")
                self.project = Project()

    def save_project_callback(self) -> None:
        path = self.save_filedialog(".raveproj", [("RAVE Project", "*.raveproj")])
        if path is not None:
            result = save_project(path, self.project)
            if not result:
                print("Failed to save project")

    def open_window_callback(self, window_type: WindowType) -> None:
        windows = {
            WindowType.PROJECT_OVERVIEW: self.project_overview_window,
            WindowType.SCRIPTING: self.scripting_window,
        }

        window = windows[window_type]
        window.close() if window.opened else window.open()

    def fullscreen_callback(self) -> None:
        self.wnd.fullscreen = not self.wnd.fullscreen

    def exit_callback(self) -> None:
        self.wnd.close()

    def script_changed_callback(self) -> None:
        uniforms = self.shader_viewer.compile(self.ctx, self.project)

        if uniforms is None:
            return

        # update uniform values within project
        # this is my attempt at maintaining history of uniforms,
        #   whether it works without bugs? im not yet convinced.
        fields = []
        for u in uniforms:
            if u.name in EXPOSED_UNIFORMS:
                continue

            match = next(
                (item for item in self.project.uniform_fields if item.name == u.name),
                None,
            )

            if match is not None:
                fields.append(
                    UniformField(
                        u.name, u.fmt, match.value, match.min_value, match.max_value
                    )
                )
            else:
                fields.append(UniformField(u.name, u.fmt, u.value, 0.0, 1.0))

        self.project.uniform_fields = fields

    def update_uniforms_callback(
        self, program: moderngl.Program, time: float, timeframe: float
    ) -> None:
        #
        if "rTime" in program:
            program["rTime"] = time

        if "rFrameTime" in program:
            program["rFrameTime"] = frametime

        # ui exposed uniforms
        for u in self.project.uniform_fields:
            if u.name in program:
                if isinstance(u.value, bytes):
                    program[u.name].write(u.value)
                else:
                    program[u.name] = u.value

    # rendering methods
    def draw_main_menu_bar(self) -> None:
        with imgui.begin_main_menu_bar() as menu_bar:
            with imgui.begin_menu("File") as file_menu:
                if file_menu.opened:
                    clicked, _ = imgui.menu_item("Open Project", "Ctrl+O")
                    if clicked:
                        self.load_project_callback()

                    clicked, _ = imgui.menu_item("Save Project", "Ctrl+S")
                    if clicked:
                        self.save_project_callback()

                    imgui.separator()

                    clicked, _ = imgui.menu_item("Exit", "Alt+F4")
                    if clicked:
                        self.exit_callback()

            with imgui.begin_menu("Window") as window_menu:
                if window_menu.opened:
                    clicked, _ = imgui.menu_item("Fullscreen", "F11")
                    if clicked:
                        self.fullscreen_callback()

                    imgui.separator()

                    clicked, _ = imgui.menu_item("Project Overview", "F1")
                    if clicked:
                        self.open_window_callback(WindowType.PROJECT_OVERVIEW)

                    clicked, _ = imgui.menu_item("Scripting", "F2")
                    if clicked:
                        self.open_window_callback(WindowType.SCRIPTING)

                    clicked, _ = imgui.menu_item("Live Control", "F3")
                    if clicked:
                        self.open_window_callback(WindowType.LIVE_CONTROL)

    def draw_windows(self, time: float, frametime: float) -> None:
        for window in self.windows:
            window.render(time=time, frametime=frametime, project=self.project)

    def render(self, time: float, frametime: float) -> None:
        self.shader_viewer.render(time, frametime)
        self.render_ui(time, frametime)

    def render_ui(self, time: float, frametime: float) -> None:
        imgui.new_frame()

        self.draw_windows(time, frametime)
        self.draw_main_menu_bar()

        imgui.render()
        self._imgui_renderer.render(imgui.get_draw_data())
        imgui.end_frame()

    # window event methods
    def resize(self, width: int, height: int):
        self.aspect_ratio = width / height
        imgui.get_io().display_size = width, height
        self._imgui_renderer.resize(width, height)
        super().resize(width, height)

    def key_event(self, key, action, modifiers) -> None:
        self._imgui_renderer.key_event(key, action, modifiers)

        if action == "ACTION_PRESS":
            if not modifiers.shift and not modifiers.ctrl and not modifiers.alt:
                # no modifiers applied
                if key == self.wnd.keys.F1:
                    self.open_window_callback(WindowType.PROJECT_OVERVIEW)
                if key == self.wnd.keys.F2:
                    self.open_window_callback(WindowType.SCRIPTING)
                if key == self.wnd.keys.F3:
                    self.open_window_callback(WindowType.LIVE_CONTROL)

            elif not modifiers.shift and modifiers.ctrl and not modifiers.alt:
                # only CTRL
                if key == self.wnd.keys.O:
                    self.load_project_callback()
                elif key == self.wnd.keys.S:
                    self.save_project_callback()

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
        super().close()
