from collections.abc import Mapping
from dataclasses import dataclass

from mutually_assured_draw.game_runner import play_game
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Outcome, Player
from mutually_assured_draw.players.base import PlayerInterface


@dataclass(frozen=True, slots=True)
class MatchLog:
    starting_player: Player
    moves: tuple[Cell, ...]
    final: Outcome

    def __str__(self):
        return f"{self.starting_player}: {', '.join(str(c.value) for c in self.moves)} -> {self.final}"


def play_match(
    players: Mapping[Player, PlayerInterface],
    initial_state: GameState | None = None,
) -> MatchLog:
    def record_move(_state: GameState, move: Cell) -> None:
        moves.append(move)

    moves: list[Cell] = []
    final_state = play_game(
        players=players,
        initial_state=initial_state,
        move_observer=record_move,
    )
    return MatchLog(
        starting_player=initial_state.current_player
        if initial_state is not None
        else Player.X,
        moves=tuple(moves),
        final=final_state.outcome,
    )
