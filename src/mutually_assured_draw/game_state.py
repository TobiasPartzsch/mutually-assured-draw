from dataclasses import dataclass

from .board import Board
from .game_types import Cell, Outcome, Player


@dataclass(frozen=True)
class GameState:
    board: Board
    current_player: Player

    @classmethod
    def new_game(cls, starting_player: Player = Player.X) -> "GameState":
        return cls(board=Board.empty(), current_player=starting_player)

    @property
    def outcome(self) -> Outcome:
        winner = self.board.winner
        if winner is Player.X:
            return Outcome.X_WINS
        if winner is Player.O:
            return Outcome.O_WINS
        if self.board.is_full:
            return Outcome.DRAW
        return Outcome.IN_PROGRESS

    @property
    def is_over(self) -> bool:
        return self.outcome is not Outcome.IN_PROGRESS

    def make_move(self, cell: Cell) -> "GameState":
        if self.is_over:
            raise ValueError(f"Game is already over: {self.outcome.name}")

        next_board = self.board.place(cell, self.current_player)
        return GameState(
            board=next_board,
            current_player=self.current_player.opponent,
        )
