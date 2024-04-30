import audioop
import numpy as np
import pyaudiowpatch as pyaudio

from typing import Any, List


CHUNK_SIZE: int = 1024


class AudioSource:
    _src: pyaudio.PyAudio
    _stream: pyaudio.Stream
    _buffer: List

    rms: float
    fft: List[float]

    def __init__(self) -> None:
        self._src = pyaudio.PyAudio()
        self._stream = None
        self.rms = 0.0
        self.fft = np.array([], dtype=np.float32)
        self._buffer = np.array([], dtype=np.int16)

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
        self.rms = audioop.rms(in_data, 2) / 32767.0

        # fft
        self._buffer = np.append(self._buffer, np.frombuffer(in_data, dtype=np.int16))
        if len(self._buffer) >= CHUNK_SIZE:
            chunk = self._buffer[:CHUNK_SIZE]

            res = np.abs(np.fft.fft(chunk) / CHUNK_SIZE)
            self.fft = res[: len(res) // 2]

            self._buffer = self._buffer[CHUNK_SIZE:]

        return (in_data, pyaudio.paContinue)
