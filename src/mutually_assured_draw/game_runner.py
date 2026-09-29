from collections.abc import Callable, Mapping

from .game_state import GameState
from .game_types import Cell, Player
from .players import PlayerInterface

StateObserver = Callable[[GameState], None]
MoveObserver = Callable[[GameState, Cell], None]


def play_game(
    players: Mapping[Player, PlayerInterface],
    initial_state: GameState | None = None,
    observer: StateObserver | None = None,
    move_observer: MoveObserver | None = None,
) -> GameState:
    """Run turns between players until the game concludes, returning the final state."""
    state = initial_state if initial_state is not None else GameState.new_game()

    if observer is not None:
        observer(state)

    while not state.is_over:
        current_agent = players[state.current_player]
        move = current_agent.select_move(state)

        if move_observer is not None:
            move_observer(state, move)

        state = state.make_move(move)

        if observer is not None:
            observer(state)

    return state
