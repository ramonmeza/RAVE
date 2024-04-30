import abc
import imgui


class Window(abc.ABC):
    title: str
    closable: bool
    opened: bool

    def __init__(self, title: str, closable: bool = False) -> None:
        self.title = title
        self.closable = closable
        self.opened = False

    def render(self) -> None:
        if self.opened:
            with imgui.begin(self.title, closable=self.closable) as window:
                self.opened = window.opened
                self.draw()

    def open(self) -> None:
        self.opened = True

    def close(self) -> None:
        self.opened = False

    @abc.abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
