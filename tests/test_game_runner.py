from mutually_assured_draw.board import Board
from mutually_assured_draw.game_runner import play_game
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Outcome, Player


class ScriptedPlayer:
    """A deterministic player stub yielding pre-planned moves."""

    def __init__(self, moves: list[Cell]) -> None:
        self.moves = iter(moves)

    def select_move(self, state: GameState) -> Cell:
        return next(self.moves)


def test_play_game_stops_immediately_on_win() -> None:
    # Give surplus moves that would raise an error or alter state if played
    player_x = ScriptedPlayer(
        [Cell.TOP_LEFT, Cell.TOP_CENTER, Cell.TOP_RIGHT, Cell.BOTTOM_RIGHT]
    )
    player_o = ScriptedPlayer([Cell.MIDDLE_LEFT, Cell.MIDDLE_CENTER, Cell.BOTTOM_LEFT])

    observed_states: list[GameState] = []

    final_state = play_game(
        players={Player.X: player_x, Player.O: player_o},
        observer=observed_states.append,
    )

    assert final_state.outcome is Outcome.X_WINS
    # Initial state + 5 moves = 6 observed states
    assert len(observed_states) == 6
    # Ensure neither player was asked for moves past game end
    assert list(player_x.moves) == [Cell.BOTTOM_RIGHT]
    assert list(player_o.moves) == [Cell.BOTTOM_LEFT]


def test_play_game_from_intermediate_state() -> None:
    # Board already has two moves played:
    # X - -
    # - O -
    # - - -
    initial = GameState(
        board=Board.from_string("X---O----"),
        current_player=Player.X,
    )

    player_x = ScriptedPlayer([Cell.TOP_CENTER, Cell.TOP_RIGHT])
    player_o = ScriptedPlayer([Cell.BOTTOM_LEFT])

    final_state = play_game(
        players={Player.X: player_x, Player.O: player_o},
        initial_state=initial,
    )

    assert final_state.outcome is Outcome.X_WINS
    assert final_state.board.cell_at(Cell.TOP_RIGHT).value == Player.X.value


def test_play_game_already_terminal_state() -> None:
    # Terminal board where X has already won the top row:
    # X X X
    # O O -
    # - - -
    terminal_state = GameState(
        board=Board.from_string("XXXOO----"),
        current_player=Player.O,
    )

    # Empty move list: any call to next() would raise StopIteration
    player_x = ScriptedPlayer([])
    player_o = ScriptedPlayer([])

    observed: list[GameState] = []

    final_state = play_game(
        players={Player.X: player_x, Player.O: player_o},
        initial_state=terminal_state,
        observer=observed.append,
    )

    assert final_state == terminal_state
    assert final_state.outcome is Outcome.X_WINS
    assert len(observed) == 1


def test_play_game_notifies_move_observer() -> None:
    player_x = ScriptedPlayer([Cell.TOP_LEFT, Cell.TOP_CENTER, Cell.TOP_RIGHT])
    player_o = ScriptedPlayer([Cell.MIDDLE_LEFT, Cell.MIDDLE_CENTER])

    observed_moves: list[tuple[GameState, Cell]] = []

    final_state = play_game(
        players={Player.X: player_x, Player.O: player_o},
        move_observer=lambda state, move: observed_moves.append((state, move)),
    )

    assert final_state.outcome is Outcome.X_WINS
    assert [move for _, move in observed_moves] == [
        Cell.TOP_LEFT,
        Cell.MIDDLE_LEFT,
        Cell.TOP_CENTER,
        Cell.MIDDLE_CENTER,
        Cell.TOP_RIGHT,
    ]
    assert [state.current_player for state, _ in observed_moves] == [
        Player.X,
        Player.O,
        Player.X,
        Player.O,
        Player.X,
    ]
