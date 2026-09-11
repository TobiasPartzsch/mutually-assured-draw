from .game_state import GameState
from .game_types import Cell, Outcome, Player, Score

WIN_SCORE = len(Cell)
DRAW_SCORE = 0


def terminal_score(state: GameState, perspective: Player) -> Score:
    """Score a terminal GameState from `perspective`'s point of view, favoring
    quicker wins and slower losses. `state` must represent a finished game."""
    if state.outcome is Outcome.DRAW:
        return Score(DRAW_SCORE)

    winner = state.board.winner()
    depth = len(state.board.cells) - len(state.board.available_cells)
    if winner is perspective:
        return Score(WIN_SCORE - depth)
    return Score(-(WIN_SCORE - depth))
