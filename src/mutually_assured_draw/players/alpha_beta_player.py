from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player, Score
from mutually_assured_draw.scoring import terminal_score


class AlphaBetaPlayer:
    alpha: float = float("-inf")
    beta: float = float("inf")

    def select_move(self, state: GameState) -> Cell:
        if state.is_over:
            raise ValueError(f"Game is already over: {state.outcome.name}")

        best_score: Score | None = None
        best_cell: Cell | None = None
        for cell in state.board.available_cells:
            score = AlphaBetaPlayer._alpha_beta(
                state.make_move(cell),
                state.current_player,
            )
            if best_score is None or score > best_score:
                best_score = score
                best_cell = cell
        assert best_cell is not None
        return best_cell

    @staticmethod
    def _alpha_beta(
        state: GameState,
        perspective: Player,
        alpha: Score | None = None,
        beta: Score | None = None,
    ) -> Score:
        if state.is_over:
            return terminal_score(state, perspective)

        scores: list[Score] = []

        for cell in state.board.available_cells:
            score = AlphaBetaPlayer._alpha_beta(
                state.make_move(cell),
                perspective,
                alpha,
                beta,
            )
            scores.append(score)

            if state.current_player is perspective:
                alpha = score if alpha is None else max(alpha, score)
            else:
                beta = score if beta is None else min(beta, score)

            if alpha is not None and beta is not None and alpha >= beta:
                break

        return Score(
            max(scores) if state.current_player is perspective else min(scores)
        )
