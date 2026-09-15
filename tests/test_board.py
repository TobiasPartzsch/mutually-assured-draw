import pytest

from mutually_assured_draw.board import Board
from mutually_assured_draw.game_types import Cell, Mark, Player


def test_empty_board_has_no_winner() -> None:
    assert Board.empty().winner is None


def test_x_wins_top_row() -> None:
    board = Board.empty()
    board = board.place(Cell.TOP_LEFT, Player.X)
    board = board.place(Cell.TOP_CENTER, Player.X)
    board = board.place(Cell.TOP_RIGHT, Player.X)

    assert board.winner is Player.X


def test_o_wins_center_column() -> None:
    board = Board.empty()
    board = board.place(Cell.TOP_CENTER, Player.O)
    board = board.place(Cell.MIDDLE_CENTER, Player.O)
    board = board.place(Cell.BOTTOM_CENTER, Player.O)

    assert board.winner is Player.O


def test_no_win_partial_board() -> None:
    board = Board.empty()
    board = board.place(Cell.TOP_LEFT, Player.X)
    board = board.place(Cell.TOP_CENTER, Player.O)

    assert board.winner is None


def test_empty_board_is_not_full() -> None:
    assert not Board.empty().is_full


def test_partially_filled_board_is_not_full() -> None:
    board = Board.empty().place(Cell.TOP_LEFT, Player.X)
    assert not board.is_full


def test_full_board_draw() -> None:
    # X O X
    # X X O
    # O X O
    moves = (
        (Cell.TOP_LEFT, Player.X),
        (Cell.TOP_CENTER, Player.O),
        (Cell.TOP_RIGHT, Player.X),
        (Cell.MIDDLE_LEFT, Player.X),
        (Cell.MIDDLE_CENTER, Player.X),
        (Cell.MIDDLE_RIGHT, Player.O),
        (Cell.BOTTOM_LEFT, Player.O),
        (Cell.BOTTOM_CENTER, Player.X),
        (Cell.BOTTOM_RIGHT, Player.O),
    )
    board = Board.empty()
    for cell, player in moves:
        board = board.place(cell, player)

    assert board.is_full
    assert board.winner is None


def test_serialize_empty_board() -> None:
    assert Board.empty().serialize() == "---------"


def test_serialize_and_from_string_round_trip() -> None:
    raw = "X-O-X--O-"
    board = Board.from_string(raw)

    assert board.serialize() == raw
    assert board.cell_at(Cell.TOP_LEFT) is Mark.X
    assert board.cell_at(Cell.TOP_CENTER) is Mark.EMPTY
    assert board.cell_at(Cell.TOP_RIGHT) is Mark.O


def test_from_string_invalid_length_raises() -> None:
    with pytest.raises(ValueError, match="must have length 9"):
        Board.from_string("XO")


def test_from_string_invalid_char_raises() -> None:
    with pytest.raises(ValueError, match="Invalid character"):
        Board.from_string("X-O-?--O-")


def test_board_str_formatting() -> None:
    board = Board.from_string("X-O-X--O-")
    expected = " X |   | O \n---+---+---\n   | X |   \n---+---+---\n   | O |   "
    assert str(board) == expected


def test_available_cells_empty_board():
    board = Board.empty()
    assert board.available_cells == list(Cell)


def test_available_cells_full_board():
    board = Board.from_string("XOXOXOXOX")
    assert board.available_cells == []


def test_available_cells_partial_board():
    board = Board.from_string("XO-------")
    assert board.available_cells == [
        Cell.TOP_RIGHT,
        Cell.MIDDLE_LEFT,
        Cell.MIDDLE_CENTER,
        Cell.MIDDLE_RIGHT,
        Cell.BOTTOM_LEFT,
        Cell.BOTTOM_CENTER,
        Cell.BOTTOM_RIGHT,
    ]
