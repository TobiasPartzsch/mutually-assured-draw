from mutually_assured_draw.players.alpha_beta_player import AlphaBetaPlayer
from mutually_assured_draw.tournament import Participant, play_head_to_head


def test_play_head_to_head_alpha_beta_draws() -> None:
    first = Participant("first", AlphaBetaPlayer())
    second = Participant("second", AlphaBetaPlayer())

    result = play_head_to_head(first, second, games_per_side=1)

    assert result.first == "first"
    assert result.second == "second"
    assert result.first_wins == 0
    assert result.second_wins == 0
    assert result.draws == 2
