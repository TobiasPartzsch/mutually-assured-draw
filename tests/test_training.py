import random
from dataclasses import dataclass

import pytest

from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player
from mutually_assured_draw.players import QLearningPlayer
from mutually_assured_draw.training import (
    reward_for_transition,
    train_against_opponent,
    train_self_play,
)


@dataclass(frozen=True)
class FixedMovePlayer:
    move: Cell

    def select_move(self, state: GameState) -> Cell:
        return self.move


def test_train_self_play_populates_q_table():
    learner = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1.0,
        rng=random.Random(0),
    )

    train_self_play(learner, episodes=1)

    assert learner.q_table


def test_train_self_play_with_zero_episodes_does_not_change_q_table():
    learner = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1.0,
        rng=random.Random(0),
    )

    train_self_play(learner, episodes=0)

    assert learner.q_table == {}


def test_learn_non_terminal_transition_adds_own_future_value():
    state = GameState.new_game()
    action = Cell.MIDDLE_CENTER

    next_state = GameState(
        board=Board.from_string("X--------"),
        current_player=Player.X,
    )
    assert next_state.current_player is state.current_player
    assert not next_state.is_over

    next_state_key = next_state.board.serialize()
    best_action = Cell.MIDDLE_CENTER

    player = QLearningPlayer(
        learning_rate=1.0,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
        q_table={(next_state_key, best_action): 0.8},
    )

    reward = reward_for_transition(state, next_state)

    player.learn(
        state=state,
        action=action,
        reward=reward,
        next_state=next_state,
    )

    key = (state.board.serialize(), action)
    assert player.q_table[key] == pytest.approx(0.72)


board_one_move_from_win = "XX-OO----"


def test_train_against_opponent_learns_from_immediate_loss():

    initial_state = GameState(
        board=Board.from_string(board_one_move_from_win),
        current_player=Player.X,
    )
    learner_action = Cell.BOTTOM_LEFT

    learner = QLearningPlayer(
        learning_rate=1.0,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
        q_table={(board_one_move_from_win, learner_action): 0.5},
    )

    opponent = FixedMovePlayer(Cell.MIDDLE_RIGHT)

    train_against_opponent(
        learner=learner,
        opponent=opponent,
        learner_player=Player.X,
        episodes=1,
        initial_state=initial_state,
    )

    key = (initial_state.board.serialize(), learner_action)
    assert learner.q_table[key] == -1.0


def test_train_against_opponent_learns_from_immediate_win():
    initial_state = GameState(
        board=Board.from_string("XX-OO----"),
        current_player=Player.X,
    )
    learner_action = Cell.TOP_RIGHT

    learner = QLearningPlayer(
        learning_rate=1.0,
        discount_factor=0.9,
        exploration_rate=0.0,
        rng=random.Random(0),
        q_table={(board_one_move_from_win, learner_action): 0.5},
    )
    opponent = FixedMovePlayer(Cell.MIDDLE_RIGHT)

    train_against_opponent(
        learner=learner,
        opponent=opponent,
        learner_player=Player.X,
        episodes=1,
        initial_state=initial_state,
    )

    key = (initial_state.board.serialize(), learner_action)
    assert learner.q_table[key] == 1.0
