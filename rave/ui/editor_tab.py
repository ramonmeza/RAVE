import abc
import imgui


class EditorTab(abc.ABC):
    title: str

    def __init__(self, title: str) -> None:
        self.title = title

    def render(self) -> None:
        with imgui.begin_tab_item(self.title) as t:
            if t.selected:
                self.draw()

    @abc.abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
