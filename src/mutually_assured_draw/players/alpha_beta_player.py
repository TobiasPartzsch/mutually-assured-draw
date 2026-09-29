from dataclasses import dataclass, field
from typing import ClassVar

from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player, Score
from mutually_assured_draw.scoring import terminal_score


@dataclass(slots=True)
class AlphaBetaPlayer:
    alpha: ClassVar[float] = float("-inf")
    beta: ClassVar[float] = float("inf")
    _cache: dict[tuple[str, Player, Player], Score] = field(
        default_factory=dict[tuple[str, Player, Player], Score],
        init=False,
        repr=False,
    )

    def select_move(self, state: GameState) -> Cell:
        if state.is_over:
            raise ValueError(f"Game is already over: {state.outcome.name}")

        best_score: Score | None = None
        best_cell: Cell | None = None
        for cell in state.board.available_cells:
            score = self._alpha_beta(
                state.make_move(cell),
                state.current_player,
            )
            if best_score is None or score > best_score:
                best_score = score
                best_cell = cell
        assert best_cell is not None
        return best_cell

    def _alpha_beta(
        self,
        state: GameState,
        perspective: Player,
        alpha: Score | None = None,
        beta: Score | None = None,
    ) -> Score:
        key = (state.board.serialize(), state.current_player, perspective)

        if state.is_over:
            score = terminal_score(state, perspective)
            self._cache[key] = score
            return score

        cached_score = self._cache.get(key)
        if cached_score is not None:
            return cached_score

        scores: list[Score] = []
        cut_off = False

        for cell in state.board.available_cells:
            score = self._alpha_beta(
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
                cut_off = True
                break

        result = Score(
            max(scores) if state.current_player is perspective else min(scores)
        )

        if not cut_off:
            self._cache[key] = result

        return result
