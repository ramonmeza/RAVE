import tkinter as tk

from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import List, Tuple


GLSL_FILES_FILTER = ("OpenGL Shading Language (GLSL)", "*.glsl")
ALL_FILES_FILTER = ("All files", "*.*")


def open_filedialog(filetypes: List[Tuple[str, ...]] = [ALL_FILES_FILTER]) -> str:
    root = tk.Tk()
    root.withdraw()
    path = askopenfilename(filetypes=filetypes)
    return path if path else None


def save_filedialog(
    defaultextension: str,
    confirmoverwrite: bool = True,
    filetypes: List[Tuple[str, ...]] = [ALL_FILES_FILTER],
) -> None:
    root = tk.Tk()
    root.withdraw()
    path = asksaveasfilename(
        confirmoverwrite=confirmoverwrite,
        defaultextension=defaultextension,
        filetypes=filetypes,
    )
    return path if path else None
