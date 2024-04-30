import imgui
import re

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
        super().__init__("Login", True)
        self._submit_callback = submit_callback
        self._register_callback = register_callback

        self.email_value = ""
        self.password_value = ""

    def is_valid_email(self, email: str) -> bool:
        # Regular expression pattern for validating email addresses
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def draw(self) -> None:
        with imgui.begin_group():
            _, self.email_value = imgui.input_text_with_hint(
                "Email",
                "your@email.com",
                self.email_value,
                flags=imgui.INPUT_TEXT_AUTO_SELECT_ALL,
            )
            _, self.password_value = imgui.input_text_with_hint(
                "Password",
                "password",
                self.password_value,
                flags=imgui.INPUT_TEXT_AUTO_SELECT_ALL
                | imgui.INPUT_TEXT_PASSWORD
                | imgui.INPUT_TEXT_CHARS_NO_BLANK,
            )

            disabled: bool = not self.is_valid_email(self.email_value) or not bool(
                self.password_value
            )
            if disabled:
                imgui.internal.push_item_flag(imgui.internal.ITEM_DISABLED, True)
                imgui.push_style_var(imgui.STYLE_ALPHA, imgui.get_style().alpha * 0.5)

            btn_clicked = imgui.button("Login")

            if btn_clicked and not disabled and self._submit_callback is not None:
                self._submit_callback(self.email_value, self.password_value)

            if disabled:
                imgui.internal.pop_item_flag()
                imgui.pop_style_var()

            imgui.same_line()

            if imgui.button("Register"):
                self._register_callback(self.email_value, self.password_value)
