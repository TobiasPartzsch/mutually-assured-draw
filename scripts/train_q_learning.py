import random

from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Player
from mutually_assured_draw.players.q_learning_player import QLearningPlayer
from training import train_self_play


def main() -> None:
    learner = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1.0,
        rng=random.Random(0),
    )

    episodes = 50_000
    train_self_play(learner, episodes)

    state = GameState(
        board=Board.from_string("XX-OO----"),
        current_player=Player.X,
    )
    key = (state.board.serialize(), Cell.TOP_RIGHT)
    value = learner.q_table.get(key, 0.0)

    print(f"Episodes: {episodes:,}")
    print(f"Q({state.board.serialize()!r}, {Cell.TOP_RIGHT.name}) = {value:.3f}")
    print(f"Q({state.board.serialize()!r}, {Cell.MIDDLE_CENTER.name}) = {value:.3f}")
    print(f"Q-table entries: {len(learner.q_table):,}")


if __name__ == "__main__":
    main()
