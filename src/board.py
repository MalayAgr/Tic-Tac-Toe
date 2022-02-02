from __future__ import annotations

from collections import Iterator
from enum import Enum
from typing import NamedTuple

from rich import box
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class _Marker(NamedTuple):
    emoji: str
    background: str = ""


class Marker(Enum):
    value: _Marker
    CROSS = _Marker("\N{CROSS MARK}", "purple3")
    NOUGHT = _Marker("\N{HEAVY LARGE CIRCLE}", "navy_blue")
    EMPTY = _Marker("\N{BLACK QUESTION MARK ORNAMENT}")

    @property
    def emoji(self) -> str:
        return self.value.emoji


class Cell:
    def __init__(self, i: int = 0, j: int = 0) -> None:
        self.marker: Marker = Marker.EMPTY
        self.pos = (i, j)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(marker={self.marker})"

    def __str__(self) -> str:
        return self.__repr__()

    def __rich__(self) -> RenderableType:
        marker = self.marker.value
        return Panel(
            Text(marker.emoji, style=f"on {marker.background}", justify="center"),
            box=box.DOUBLE,
            title=str(self.pos),
        )


class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.cells = {(i, j): Cell(i, j) for i in range(size) for j in range(size)}

    def update_cell(self, i: int, j: int, marker: Marker) -> None:
        cell = self.cells.get((i, j))
        if cell is None:
            raise ValueError("Indices are out of bounds for the board.")
        cell.marker = marker

    @property
    def winning_positions(self) -> Iterator[list[Marker]]:
        cells, size = self.cells, self.size

        # rows
        for row in range(size):
            yield [cells[(row, col)].marker for col in range(size)]

        # columns
        for col in range(size):
            yield [cells[(row, col)].marker for row in range(size)]

        # Diagonal from top left
        yield [cells[(i, i)].marker for i in range(size)]

        # Diagonal from top right
        yield [cells[(i, size - 1 - i)].marker for i in range(size)]

    def is_full(self) -> bool:
        return not any(cell.marker is Marker.EMPTY for cell in self.cells.values())

    def __rich__(self) -> RenderableType:
        size, cells = self.size, self.cells
        grid = Table.grid(expand=True)

        for _ in range(size):
            grid.add_column()

        for i in range(size):
            grid.add_row(*(cells[(i, j)] for j in range(size)))

        return grid
