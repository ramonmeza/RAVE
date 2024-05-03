import imgui

from typing import Callable, List, Optional

from rave.project import Project
from rave.tool_window import ToolWindow


ApplyAudioConfigCallback = Optional[Callable[[int, int, int, int], None]]


SAMPLE_RATES: List[str] = ["44100", "48000"]
CHANNELS: List[str] = ["mono", "stereo"]


class AudioConfigWindow(ToolWindow):
    all_devices: List[str]
    current_device_index: int
    sample_rate_index: int
    num_channels_index: int
    frames_per_buffer: int

    apply_audio_config_callback: ApplyAudioConfigCallback

    def __init__(
        self,
        default_device_index: int = 0,
        apply_audio_config_callback: ApplyAudioConfigCallback = None,
        opened: bool = True,
    ) -> None:
        super().__init__("Audio Config", opened)
        self.all_devices = []
        self.current_device_index = default_device_index
        self.sample_rate_index = 0
        self.num_channels_index = 0
        self.frames_per_buffer = 1024
        self.apply_audio_config_callback = apply_audio_config_callback

    def set_all_devices(self, all_devices: List[str]) -> None:
        self.all_devices = all_devices

    def draw(self, project: Project, **kwargs) -> None:
        _, self.current_device_index = imgui.combo(
            "Device", self.current_device_index, self.all_devices
        )
        _, self.sample_rate_index = imgui.combo(
            "Sample Rate (Hz)", self.sample_rate_index, SAMPLE_RATES
        )
        _, self.num_channels_index = imgui.combo(
            "Channels", self.num_channels_index, CHANNELS
        )
        _, self.frames_per_buffer = imgui.input_int(
            "Frames Per Buffer", self.frames_per_buffer
        )

        if imgui.button("Apply") and self.apply_audio_config_callback is not None:
            self.apply_audio_config_callback(
                input_device_index=self.current_device_index,
                sample_rate=int(SAMPLE_RATES[self.sample_rate_index]),
                channels=(
                    2 if CHANNELS[self.num_channels_index].lower() == "stereo" else 1
                ),
                frames_per_buffer=self.frames_per_buffer,
            )
