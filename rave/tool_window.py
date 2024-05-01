import abc
import imgui


class ToolWindow(abc.ABC):
    title: str
    opened: bool
    closable: bool

    def __init__(self, title: str, opened: bool = True, closable: bool = True) -> None:
        self.title = title
        self.opened = opened
        self.closable = closable

    def open(self) -> None:
        self.opened = True

    def close(self) -> None:
        self.opened = False

    @abc.abstractmethod
    def draw(self, **kwargs) -> None:
        raise NotImplementedError

    def render(self, time: float = 0.0, frametime: float = 0.0, **kwargs) -> None:
        if self.opened:
            with imgui.begin(self.title, closable=self.closable) as w:
                self.opened = w.opened
                self.draw(time=time, frametime=frametime, **kwargs)
