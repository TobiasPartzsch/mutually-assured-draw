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


def test_empty_board_is_not_full() -> None:
    assert not Board.empty().is_full()


def test_partially_filled_board_is_not_full() -> None:
    board = Board.empty().place(Cell.TOP_LEFT, Player.X)
    assert not board.is_full()


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

    assert board.is_full()
    assert board.winner() is None
