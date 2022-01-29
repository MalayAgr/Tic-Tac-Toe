from __future__ import annotations

from collections import namedtuple
from enum import Enum

from rich import box
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

_Marker = namedtuple("marker", ["emoji", "background"])


class Marker(Enum):
    CROSS = _Marker("\N{CROSS MARK}", "green")
    NOUGHT = _Marker("\N{HEAVY LARGE CIRCLE}", "yellow")
    EMPTY = _Marker("\N{BLACK QUESTION MARK ORNAMENT}", "")


class Cell:
    def __init__(self, i: int = 0, j: int = 0) -> None:
        self.marker: Marker = Marker.EMPTY
        self.pos = (i, j)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(marker={self.marker})"

    def __str__(self) -> str:
        return self.__repr__()

    def __rich__(self) -> RenderableType:
        marker: _Marker = self.marker.value
        return Panel(
            Text(marker.emoji, style=f"on {marker.background}", justify="center"),
            box=box.DOUBLE,
            title=str(self.pos),
        )


class Board:
    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.cells = {(i, j): Cell(i, j) for i in range(size) for j in range(size)}

    def update_cell(self, i: int, j: int, marker: Marker):
        cell = self.cells[(i, j)]
        cell.marker = marker

    def __rich__(self) -> RenderableType:
        size, cells = self.size, self.cells
        grid = Table.grid(expand=True)

        for _ in range(size):
            grid.add_column()

        for i in range(size):
            grid.add_row(*(cells[(i, j)] for j in range(size)))

        return grid
