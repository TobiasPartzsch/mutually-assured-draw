import pytest

from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Outcome, Player


def test_new_game_defaults() -> None:
    state = GameState.new_game()

    assert state.board == Board.empty()
    assert state.current_player is Player.X
    assert state.outcome is Outcome.IN_PROGRESS
    assert not state.is_over


def test_make_move_advances_turn() -> None:
    state = GameState.new_game()
    next_state = state.make_move(Cell.TOP_LEFT)

    assert next_state.board.cell_at(Cell.TOP_LEFT).value == Player.X.value
    assert next_state.current_player is Player.O
    assert next_state.outcome is Outcome.IN_PROGRESS


def test_cannot_move_into_occupied_cell() -> None:
    state = GameState.new_game().make_move(Cell.TOP_LEFT)

    with pytest.raises(ValueError, match="already occupied"):
        state.make_move(Cell.TOP_LEFT)


def test_outcome_detects_win() -> None:
    # Set up board one move away from X winning top row:
    # X X -
    # O O -
    # - - -
    board = Board.from_string("XX-OO----")
    state = GameState(board=board, current_player=Player.X)

    winning_state = state.make_move(Cell.TOP_RIGHT)

    assert winning_state.outcome is Outcome.X_WINS
    assert winning_state.is_over


def test_outcome_detects_draw() -> None:
    # Full board draw:
    # X O X
    # X X O
    # O X O
    board = Board.from_string("XOX-XOOXO")
    state = GameState(board=board, current_player=Player.X)

    draw_state = state.make_move(Cell.MIDDLE_LEFT)

    assert draw_state.outcome is Outcome.DRAW
    assert draw_state.is_over


def test_cannot_move_after_game_is_over() -> None:
    board = Board.from_string("XXXOO----")
    state = GameState(board=board, current_player=Player.O)

    assert state.is_over
    with pytest.raises(ValueError, match="already over"):
        state.make_move(Cell.BOTTOM_RIGHT)
