import imgui
import pyaudiowpatch as pyaudio

from rave.ui.editor_tab import EditorTab
from typing import Callable, List, Optional


STREAM_ON_STARTUP: bool = False


class AudioConfigTab(EditorTab):
    _audio_drivers: List[str]
    _current_driver_index: int
    _apply_btn_callback: Callable[[int], None]

    def __init__(
        self,
        audio_drivers: List[str],
        default_driver_index: int,
        apply_btn_callback: Callable[[int], None],
    ) -> None:
        super().__init__("Audio Config")

        self._audio_drivers = audio_drivers
        self._current_driver_index = default_driver_index
        self._apply_btn_callback = apply_btn_callback

        if STREAM_ON_STARTUP:
            self._apply_btn_callback(self._current_driver_index)

    def draw(self) -> None:
        _, self._current_driver_index = imgui.combo(
            "Driver", self._current_driver_index, self._audio_drivers
        )

        btn_clicked: bool = imgui.button("Apply")
        if btn_clicked:
            self._apply_btn_callback(self._current_driver_index)
