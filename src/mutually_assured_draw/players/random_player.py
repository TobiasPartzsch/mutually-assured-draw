import random

from ..game_state import GameState
from ..game_types import Cell


class RandomPlayer:
    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def select_move(self, state: GameState) -> Cell:
        return self._rng.choice(state.board.available_cells)
