import audioop
import pyaudiowpatch as pyaudio

from typing import Any, List


class AudioSource:
    _src: pyaudio.PyAudio
    _stream: pyaudio.Stream

    rms: float
    fft: List[float]

    def __init__(self) -> None:
        self._src = pyaudio.PyAudio()
        self._stream = None
        self.rms = 0.0
        self.fft = []

    def start_stream(
        self,
        channels: int = 2,
        sample_rate: int = 44100,
        input_device_index: int = 0,
        buffer_size: int = 1024,
    ) -> None:
        if self._stream is not None:
            self._stream.close()

        self._stream = self._src.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            input_device_index=input_device_index,
            frames_per_buffer=buffer_size,
            stream_callback=self.audio_receieved,
        )

    def close(self) -> None:
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        self._src.terminate()

    def get_available_drivers(self) -> None:
        return [
            driver["name"] for driver in list(self._src.get_device_info_generator())
        ]

    def get_default_loopback_driver(self) -> None:
        return self._src.get_default_wasapi_loopback()["index"]

    def audio_receieved(self, in_data, frame_count, time_info, status) -> Any:
        # set rms
        self.rms = audioop.rms(in_data, 2)

        # set fft
        self.fft = []  # @todo

        return (in_data, pyaudio.paContinue)
