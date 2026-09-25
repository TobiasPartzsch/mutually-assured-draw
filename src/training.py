from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Outcome
from mutually_assured_draw.players.q_learning_player import QLearningPlayer


def reward_for_transition(
    state: GameState,
    next_state: GameState,
) -> float:
    if not next_state.is_over:
        return 0.0

    if next_state.outcome is Outcome.DRAW:
        return 0.0

    winner = next_state.board.winner
    return 1.0 if winner is state.current_player else -1.0


def train_self_play(
    learner: QLearningPlayer,
    episodes: int,
) -> None:
    for _ in range(episodes):
        state = GameState.new_game()

        while not state.is_over:
            action = learner.select_training_move(state)
            next_state = state.make_move(action)
            reward = reward_for_transition(state, next_state)

            learner.learn(
                state=state,
                action=action,
                reward=reward,
                next_state=next_state,
            )
            state = next_state
