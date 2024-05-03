import audioop
import numpy as np
import pyaudiowpatch as pyaudio

from typing import List


class AudioDevice:
    source: pyaudio.PyAudio
    stream: pyaudio.Stream
    audio_buffer: List

    rms: float
    fft: List[float]

    def __init__(self) -> None:
        self.source = pyaudio.PyAudio()
        self.stream = None
        self.audio_buffer = []

        self.rms = 0.0
        self.fft = []

    def start(
        self,
        input_device_index: int,
        sample_rate: int = 44100,
        channels: int = 2,
        frames_per_buffer: int = 1024,
    ) -> None:
        if self.stream is not None:
            self.stream.close()

        self.stream = self.source.open(
            input_device_index=input_device_index,
            rate=sample_rate,
            channels=channels,
            frames_per_buffer=frames_per_buffer,
            format=pyaudio.paInt16,
            input=True,
            stream_callback=self.stream_callback,
        )

    def close(self) -> None:
        if self.stream is not None:
            self.stream.close()

        self.source.terminate()

    def get_default_loopback_device_index(self) -> int:
        return self.source.get_default_wasapi_loopback()["index"]

    def get_all_devices(self) -> List[str]:
        return [x["name"] for x in self.source.get_device_info_generator()]

    def stream_callback(self, in_data, frame_count, time_info, status) -> None:
        # rms
        self.rms = audioop.rms(in_data, 2) / 32767.0

        chunk_size = self.stream._frames_per_buffer

        # fft
        self.audio_buffer = np.append(
            self.audio_buffer, np.frombuffer(in_data, dtype=np.int16)
        )
        if len(self.audio_buffer) >= chunk_size:
            chunk = self.audio_buffer[:chunk_size]

            res = np.abs(np.fft.fft(chunk) / chunk_size)
            self.fft = res[: len(res) // 2]

            self.audio_buffer = self.audio_buffer[chunk_size:]

        return (in_data, pyaudio.paContinue)

    def get_rms(self) -> float:
        return self.rms

    def get_fft(self) -> List[float]:
        return self.fft
