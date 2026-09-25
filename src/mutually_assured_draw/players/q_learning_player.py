import random
from dataclasses import dataclass, field
from typing import TypeAlias

from mutually_assured_draw.game_state import GameState

from ..game_types import Cell

StateKey: TypeAlias = str
QValue: TypeAlias = float
QKey: TypeAlias = tuple[StateKey, Cell]


def empty_q_table() -> dict[QKey, QValue]:
    return {}


@dataclass(slots=True)
class QLearningPlayer:
    learning_rate: float
    discount_factor: float
    exploration_rate: float
    rng: random.Random
    q_table: dict[QKey, QValue] = field(default_factory=empty_q_table)

    def select_move(self, state: GameState) -> Cell:
        if state.is_over:
            raise ValueError(f"Game is already over: {state.outcome.name}")

        available_cells = state.board.available_cells
        state_key = state.board.serialize()

        values_by_cell = {
            cell: self.q_table.get((state_key, cell), 0.0) for cell in available_cells
        }
        best_value = max(values_by_cell.values())
        best_cells = [
            cell for cell, value in values_by_cell.items() if value == best_value
        ]
        return self.rng.choice(best_cells)

    def select_training_move(self, state: GameState) -> Cell:
        if state.is_over:
            raise ValueError(f"Game is already over: {state.outcome.name}")

        available_cells = state.board.available_cells

        if self.rng.random() < self.exploration_rate:
            return self.rng.choice(available_cells)

        return self.select_move(state)

    def learn(
        self,
        state: GameState,
        action: Cell,
        reward: float,
        next_state: GameState,
    ) -> None:
        state_key = state.board.serialize()
        q_key = (state_key, action)
        old_value = self.q_table.get(q_key, 0.0)

        if next_state.is_over:
            target = reward
        else:
            next_state_key = next_state.board.serialize()
            best_next_value = max(
                self.q_table.get((next_state_key, next_action), 0.0)
                for next_action in next_state.board.available_cells
            )
            if next_state.current_player is state.current_player:
                target = reward + self.discount_factor * best_next_value
            else:
                target = reward - self.discount_factor * best_next_value

        self.q_table[q_key] = old_value + self.learning_rate * (target - old_value)
