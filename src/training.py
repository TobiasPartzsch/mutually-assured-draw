from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Outcome, Player
from mutually_assured_draw.players.base import PlayerInterface
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


def train_against_opponent(
    learner: QLearningPlayer,
    opponent: PlayerInterface,
    learner_player: Player,
    episodes: int,
    initial_state: GameState | None = None,
) -> None:
    for _ in range(episodes):
        if initial_state is None:
            state = GameState.new_game()
        else:
            state = initial_state

        while not state.is_over:
            if state.current_player is not learner_player:
                state = state.make_move(opponent.select_move(state))
                continue

            action = learner.select_training_move(state)
            after_learner_move = state.make_move(action)

            if after_learner_move.is_over:
                reward = reward_for_transition(state, after_learner_move)
                learner.learn(
                    state=state,
                    action=action,
                    reward=reward,
                    next_state=after_learner_move,
                )
                state = after_learner_move
                continue

            next_state = after_learner_move.make_move(
                opponent.select_move(after_learner_move)
            )
            reward = reward_for_transition(state, next_state)

            learner.learn(
                state=state,
                action=action,
                reward=reward,
                next_state=next_state,
            )
            state = next_state
