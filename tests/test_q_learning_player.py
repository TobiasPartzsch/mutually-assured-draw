import random

import pytest

from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player
from mutually_assured_draw.players.q_learning_player import QLearningPlayer


def test_select_move_with_single_available_cell():
    state = GameState(
        board=Board.from_string("XOXOXXOO-"),
        current_player=Player.X,
    )
    player = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
    )

    assert player.select_move(state) is Cell.BOTTOM_RIGHT


def test_select_move_returns_an_available_cell():
    state = GameState(
        board=Board.from_string("X-O------"),
        current_player=Player.X,
    )
    player = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
    )

    assert player.select_move(state) in state.board.available_cells


def test_select_move_chooses_uniquely_highest_valued_action():
    state = GameState(
        board=Board.from_string("X--------"),
        current_player=Player.O,
    )
    state_key = state.board.serialize()
    expected_move = Cell.MIDDLE_CENTER

    player = QLearningPlayer(
        exploration_rate=0.0,
        learning_rate=0.1,
        discount_factor=0.9,
        rng=random.Random(0),
        q_table={
            (state_key, expected_move): 0.8,
            (state_key, Cell.TOP_CENTER): 0.3,
        },
    )

    assert player.select_move(state) == expected_move


def test_select_move_breaks_equal_value_ties_among_best_cells():
    state = GameState(
        board=Board.from_string("X--------"),
        current_player=Player.O,
    )
    state_key = state.board.serialize()
    tied_cells = (Cell.TOP_CENTER, Cell.MIDDLE_CENTER)

    player = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
        q_table={
            (state_key, Cell.TOP_CENTER): 1.0,
            (state_key, Cell.MIDDLE_CENTER): 1.0,
        },
    )

    assert player.select_move(state) in tied_cells


def test_select_move_rejects_finished_game():
    state = GameState(
        board=Board.from_string("XXXOOXXOO"),
        current_player=Player.O,
    )
    player = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
    )

    with pytest.raises(ValueError, match="Game is already over: X_WINS"):
        player.select_move(state)


def test_select_training_move_with_zero_exploration_is_greedy():
    state = GameState(
        board=Board.from_string("X--------"),
        current_player=Player.O,
    )
    state_key = state.board.serialize()

    player = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
        q_table={(state_key, Cell.MIDDLE_CENTER): 1.0},
    )

    assert player.select_training_move(state) is Cell.MIDDLE_CENTER


def test_learn_terminal_transition_stores_reward():
    state = GameState.new_game()
    action = Cell.MIDDLE_CENTER
    next_state = state.make_move(action)

    player = QLearningPlayer(
        learning_rate=1.0,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
    )

    player.learn(
        state=state,
        action=action,
        reward=1.0,
        next_state=next_state,
    )

    assert player.q_table[(state.board.serialize(), action)] == 1.0


def test_learn_terminal_win_uses_reward_as_target():
    state = GameState(
        board=Board.from_string("XX-OO----"),
        current_player=Player.X,
    )
    action = Cell.TOP_RIGHT
    next_state = state.make_move(action)

    assert next_state.is_over

    player = QLearningPlayer(
        learning_rate=1.0,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
    )

    player.learn(
        state=state,
        action=action,
        reward=1.0,
        next_state=next_state,
    )

    key = (state.board.serialize(), action)
    assert player.q_table[key] == 1.0


def test_learn_non_terminal_transition_negates_opponent_value():
    state = GameState.new_game()
    action = Cell.MIDDLE_CENTER
    next_state = state.make_move(action)

    assert not next_state.is_over

    next_state_key = next_state.board.serialize()
    opponent_best_action = Cell.TOP_LEFT

    player = QLearningPlayer(
        learning_rate=1.0,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
        q_table={
            (next_state_key, opponent_best_action): 0.8,
        },
    )

    player.learn(
        state=state,
        action=action,
        reward=0.0,
        next_state=next_state,
    )

    current_key = (state.board.serialize(), action)
    assert player.q_table[current_key] == pytest.approx(-0.72)
