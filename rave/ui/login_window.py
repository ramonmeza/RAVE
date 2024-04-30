import imgui

from rave.ui.window import Window
from typing import Callable, Optional


class LoginWindow(Window):
    email_value: str
    password_value: str

    _submit_callback: Optional[Callable[[str, str], None]]
    _register_callback: Optional[Callable[[str, str], None]]

    def __init__(
        self,
        submit_callback: Optional[Callable[[str, str], None]] = None,
        register_callback: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        super().__init__("Login")
        self._submit_callback = submit_callback
        self._register_callback = register_callback

        self.email_value = ""
        self.password_value = ""

    def draw(self) -> None:
        with imgui.begin_group():
            _, self.email_value = imgui.input_text(
                "Email", self.email_value, flags=imgui.INPUT_TEXT_AUTO_SELECT_ALL
            )
            _, self.password_value = imgui.input_text(
                "Password",
                self.password_value,
                flags=imgui.INPUT_TEXT_AUTO_SELECT_ALL | imgui.INPUT_TEXT_PASSWORD,
            )

            if imgui.button("Login") and self._submit_callback is not None:
                self._submit_callback(self.email_value, self.password_value)

            imgui.same_line()

            if imgui.button("Register"):
                self._register_callback(self.email_value, self.password_value)
