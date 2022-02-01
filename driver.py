from rich.layout import Layout
from rich.prompt import Confirm, IntPrompt, Prompt

from src.board import Marker
from src.console import console
from src.game import Game


def main():
    try:
        player_1 = Prompt.ask("Enter name of first player", default="player 1")
        player_2 = Prompt.ask("Enter name of second player", default="player 2")
        size = IntPrompt.ask("Enter the size of the board. Leave b", default=3)

        input("Press ENTER to start playing.")
        console.clear()

        game = Game(players=[player_1, player_2], board_size=size)

        n_round = 1

        while True:
            console.rule("[bold red]Tic-Tac-Toe by Malay Agarwal[/bold red]")
            console.rule(f"[bold blue]Round {n_round}[/bold blue]")
            game.randomize_marker()
            game.play()

            next_round = Confirm.ask("Play another round?")
            if not next_round:
                break

            game.reset()
            console.clear()
            n_round += 1

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()


if __name__ == "__main__":
    main()
