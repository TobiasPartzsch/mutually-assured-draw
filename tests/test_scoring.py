from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Player
from mutually_assured_draw.scoring import WIN_SCORE, terminal_score


def test_terminal_score_win_for_perspective():
    state = GameState(board=Board.from_string("XXXOO----"), current_player=Player.O)
    score = terminal_score(state, perspective=Player.X)
    assert score == WIN_SCORE - 5


def test_terminal_score_loss_for_perspective():
    state = GameState(board=Board.from_string("XXXOO----"), current_player=Player.O)
    score = terminal_score(state, perspective=Player.O)
    assert score == -(WIN_SCORE - 5)


def test_terminal_score_draw():
    state = GameState(board=Board.from_string("OXOXOXXOX"), current_player=Player.X)
    score = terminal_score(state, perspective=Player.X)
    assert score == 0
