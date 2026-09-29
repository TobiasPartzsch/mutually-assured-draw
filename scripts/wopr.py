import random
from dataclasses import dataclass

from mutually_assured_draw.game_types import Player
from mutually_assured_draw.players.alpha_beta_player import AlphaBetaPlayer
from mutually_assured_draw.players.q_learning_player import QLearningPlayer
from mutually_assured_draw.tournament import Participant, play_head_to_head
from mutually_assured_draw.training import train_against_opponent


@dataclass(frozen=True, slots=True)
class TrainingConfig:
    batch_size: int = 100
    max_episodes_per_mark: int = 100_000
    evaluation_games_per_side: int = 100
    allowed_losses: int = 0


def evaluate(
    learner: QLearningPlayer,
    opponent: AlphaBetaPlayer,
    games_per_side: int,
):
    previous_exploration_rate = learner.exploration_rate
    learner.exploration_rate = 0.0

    try:
        return play_head_to_head(
            first=Participant("Q-learning", learner),
            second=Participant("Alpha-beta", opponent),
            games_per_side=games_per_side,
        )
    finally:
        learner.exploration_rate = previous_exploration_rate


def main() -> None:
    config = TrainingConfig()
    learner = QLearningPlayer(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1.0,
        rng=random.Random(0),
    )
    opponent = AlphaBetaPlayer()

    episodes_completed = 0

    while episodes_completed < config.max_episodes_per_mark:
        batch_episodes = min(
            config.batch_size,
            config.max_episodes_per_mark - episodes_completed,
        )

        train_against_opponent(
            learner=learner,
            opponent=opponent,
            learner_player=Player.X,
            episodes=batch_episodes,
        )
        train_against_opponent(
            learner=learner,
            opponent=opponent,
            learner_player=Player.O,
            episodes=batch_episodes,
        )

        episodes_completed += 2 * batch_episodes

        result = evaluate(
            learner,
            opponent,
            config.evaluation_games_per_side,
        )

        learner_losses = result.second_wins
        print(f"After {episodes_completed:,} learner games: {result}")

        if learner_losses <= config.allowed_losses:
            print("A strange game. The only winning move is not to play.")
            return

    print("Training limit reached without meeting the evaluation target.")


if __name__ == "__main__":
    main()
