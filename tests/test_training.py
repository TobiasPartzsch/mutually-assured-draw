import random

from mutually_assured_draw.players.q_learning_player import QLearningPlayer
from training import train_self_play


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
