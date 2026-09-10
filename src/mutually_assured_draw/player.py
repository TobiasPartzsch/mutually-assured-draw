from typing import Protocol

from .game_state import GameState
from .game_types import Cell


class PlayerInterface(Protocol):
    def select_move(self, state: GameState) -> Cell:
        """Given a GameState, return the selected Cell move."""
        ...
