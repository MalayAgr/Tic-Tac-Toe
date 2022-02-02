from __future__ import annotations

import itertools
import random

from rich.console import RenderableType
from rich.prompt import IntPrompt

from .board import Board, Marker
from .console import console

MARKER_MAP = {0: Marker.CROSS, 1: Marker.NOUGHT}


def _print_centered(text: RenderableType) -> None:
    console.print(text, justify="center")


class Game:
    win_msg = "[bold]Congratulations![/bold] You are the [green]winner[/green], [bold]{}![/bold] :smiley:"
    draw_msg = "[red]It's a draw! :disappointed:[/red]"
    turn_msg = "[green]It's your turn, [bold]{}[/bold] ({})"
    error_msg = "[prompt.invalid]Please make sure the {} value is between 0 and {}"

    def __init__(self, players: list[str], board_size: int = 3) -> None:
        self.board_size = board_size
        self._max_pos = board_size - 1
        self.board = Board(size=board_size)
        self._players = players
        self.players = self._players.copy()

    def randomize_marker(self) -> None:
        random.shuffle(self.players)

    def play(self) -> None:
        players, turn = self.players, 0
        while True:
            player, marker = players[turn].title(), MARKER_MAP[turn]

            _print_centered(self.turn_msg.format(player, marker.emoji))
            _print_centered(self.board)

            row, col = self._ask_cell()

            self.board.update_cell(row, col, marker)

            if self._check_winner(marker) is True:
                console.rule()
                _print_centered(self.board)
                _print_centered(self.win_msg.format(player))
                break

            if self._check_draw() is True:
                console.rule()
                _print_centered(self.board)
                _print_centered(self.draw_msg)
                break

            turn = (turn + 1) % 2
            console.rule()

    def reset(self) -> None:
        self.player = self._players.copy()
        board_size = IntPrompt.ask(
            "Leave blank for previous board size or enter a new one",
            default=self.board_size,
        )
        self.board_size = board_size
        self._max_pos = board_size - 1
        self.board = Board(size=board_size)

    def _check_winner(self, marker: Marker) -> bool:
        return any(
            all(x is marker for x in positions)
            for positions in self.board.winning_positions
        )

    def _check_draw(self) -> bool:
        conflict = {Marker.CROSS, Marker.NOUGHT}
        b = self.board
        return b.is_full() or all(conflict.issubset(pos) for pos in b.winning_positions)

    def _ask_cell(self) -> tuple[int, int]:
        maximum = self._max_pos

        while True:
            row = IntPrompt.ask("Enter the row of the cell you want to mark")

            if not 0 <= row <= maximum:
                console.print(self.error_msg.format("row", maximum))
                continue

            break

        while True:
            col = IntPrompt.ask("Enter the column")

            if not 0 <= col <= maximum:
                console.print(self.error_msg.format("column", maximum))
                continue

            break

        return row, col
