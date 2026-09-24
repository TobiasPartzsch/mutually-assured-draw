from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player, Score
from mutually_assured_draw.scoring import terminal_score


class MinimaxPlayer:
    def select_move(self, state: GameState) -> Cell:
        if state.is_over:
            raise ValueError(f"Game is already over: {state.outcome.name}")

        best_score: Score | None = None
        best_cell: Cell | None = None
        for cell in state.board.available_cells:
            score = MinimaxPlayer._minimax(
                state.make_move(cell),
                state.current_player,
            )
            if best_score is None or score > best_score:
                best_score = score
                best_cell = cell
        assert best_cell is not None
        return best_cell

    @staticmethod
    def _minimax(state: GameState, perspective: Player) -> Score:
        if state.is_over:
            return terminal_score(state, perspective)

        scores = [
            MinimaxPlayer._minimax(state.make_move(cell), perspective)
            for cell in state.board.available_cells
        ]

        if state.current_player is perspective:
            return Score(max(scores))
        return Score(min(scores))
