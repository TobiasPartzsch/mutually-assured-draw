from mutually_assured_draw.board import Board
from mutually_assured_draw.game_types import Cell, Player


def test_empty_board_has_no_winner() -> None:
    assert Board.empty().winner() is None


def test_x_wins_top_row() -> None:
    board = Board.empty()
    board = board.place(Cell.TOP_LEFT, Player.X)
    board = board.place(Cell.TOP_CENTER, Player.X)
    board = board.place(Cell.TOP_RIGHT, Player.X)

    assert board.winner() is Player.X


def test_o_wins_center_column() -> None:
    board = Board.empty()
    board = board.place(Cell.TOP_CENTER, Player.O)
    board = board.place(Cell.MIDDLE_CENTER, Player.O)
    board = board.place(Cell.BOTTOM_CENTER, Player.O)

    assert board.winner() is Player.O


def test_no_win_partial_board() -> None:
    board = Board.empty()
    board = board.place(Cell.TOP_LEFT, Player.X)
    board = board.place(Cell.TOP_CENTER, Player.O)

    assert board.winner() is None
