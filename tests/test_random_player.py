import random

import pytest

from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player
from mutually_assured_draw.players.random_player import RandomPlayer


def test_select_move_is_deterministic_with_seed():
    state = GameState.new_game()
    player = RandomPlayer(rng=random.Random(42))

    move = player.select_move(state)

    assert move == Cell.TOP_CENTER


def test_select_move_with_single_available_cell():
    board = Board.from_string("XOXOXOXO-")
    state = GameState(board=board, current_player=Player.X)
    player = RandomPlayer(rng=random.Random(1))

    move = player.select_move(state)

    assert move == Cell.BOTTOM_RIGHT


def test_select_move_raises_on_no_available_cells():
    board = Board.from_string("XOXOXOXOX")
    state = GameState(board=board, current_player=Player.X)
    player = RandomPlayer(rng=random.Random(1))

    with pytest.raises(IndexError):
        player.select_move(state)
