from __future__ import annotations

import random

from rich.console import RenderableType
from rich.prompt import IntPrompt

from .board import Board, Marker
from .console import console

MARKER_MAP = {0: Marker.CROSS, 1: Marker.NOUGHT}


def _print_centered(text: RenderableType) -> None:
    console.print(text, justify="center")


class Game:
    def __init__(self, players: list[str], board_size: int = 3) -> None:
        self.board_size = board_size
        self.board = Board(size=board_size)
        self.turn: int = 0
        self._players = players
        self.players = self._players.copy()

    def randomize_marker(self):
        random.shuffle(self.players)

    def play(self):
        players, turn = self.players, self.turn
        while True:
            _print_centered(self.board)

            player, marker = players[turn], MARKER_MAP[turn]

            row, col = self._ask_cell(players[turn])

            self.board.update_cell(row, col, marker)

            if self._check_winner(marker) is True:
                _print_centered(f"Congratulations! You are the winner, {player}!")
                break

            turn = (turn + 1) % 2
            console.rule()

    def reset(self):
        self.player = self._players.copy()
        self.turn = 0
        self.board = Board(size=self.board_size)

    def _check_winner(self, marker: Marker):
        return any(
            all(x is marker for x in positions)
            for positions in self.board.winning_positions
        )

    def _ask_cell(self, player: str) -> tuple[int, int]:
        _print_centered(f"[green]It's your turn, {player.title()}")

        maximum = self.board_size - 1
        msg = (
            "[prompt.invalid]Please make sure the {}"
            f"value is are between 0 and {maximum}"
        )

        while True:
            row = IntPrompt.ask("Enter the row of the cell you want to mark")

            if not 0 <= row <= maximum:
                console.print(msg.format("row"))
                continue

            break

        while True:
            col = IntPrompt.ask("Enter the column of the cell you want to mark")

            if not 0 <= col <= maximum:
                console.print(msg.format("col"))
                continue

            break

        return row, col
