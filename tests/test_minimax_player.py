from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Outcome, Player
from mutually_assured_draw.players.minimax_player import MinimaxPlayer


def test_select_move_with_single_available_cell():
    board = Board.from_string("XOXOXXOO-")
    state = GameState(board=board, current_player=Player.X)
    player = MinimaxPlayer()

    move = player.select_move(state)

    assert move == Cell.BOTTOM_RIGHT


def test_select_move_to_block_win():
    board = Board.from_string("XXO-O----")
    state = GameState(board=board, current_player=Player.X)
    player = MinimaxPlayer()

    move = player.select_move(state)

    assert move == Cell.BOTTOM_LEFT


def test_select_move_to_block_win_as_O():
    board = Board.from_string("OXOXO-X-X")

    state = GameState(board=board, current_player=Player.O)
    player = MinimaxPlayer()

    move = player.select_move(state)

    assert move == Cell.BOTTOM_CENTER


def test_select_move_to_win_first():
    board = Board.from_string("XX-OO----")
    state = GameState(board=board, current_player=Player.X)
    player = MinimaxPlayer()

    move = player.select_move(state)

    assert move == Cell.TOP_RIGHT


def test_select_move_to_win_fast():
    board = Board.from_string("XX-O--O--")
    state = GameState(board=board, current_player=Player.X)
    player = MinimaxPlayer()

    move = player.select_move(state)

    assert move == Cell.TOP_RIGHT


def test_game_always_ends_in_draw():
    board = Board.from_string("---------")
    state = GameState(board=board, current_player=Player.X)
    player = MinimaxPlayer()
    while not state.is_over:
        move = player.select_move(state)
        state = state.make_move(move)

    assert state.outcome == Outcome.DRAW


def test_game_always_ends_in_draw_regardless_where_x_starts():
    pattern = ["-"] * len(Cell)
    for i in range(len(Cell)):
        new = pattern[:]
        new[i] = "X"
        board = Board.from_string("".join(new))
        state = GameState(board=board, current_player=Player.O)
        player = MinimaxPlayer()
        while not state.is_over:
            move = player.select_move(state)
            state = state.make_move(move)

        assert state.outcome == Outcome.DRAW
