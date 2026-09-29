from mutually_assured_draw.arena import play_match
from mutually_assured_draw.board import Board
from mutually_assured_draw.game_state import GameState
from mutually_assured_draw.game_types import Cell, Outcome, Player
from mutually_assured_draw.players.alpha_beta_player import AlphaBetaPlayer


def test_play_match_records_moves_and_outcome() -> None:
    players = {
        Player.X: AlphaBetaPlayer(),
        Player.O: AlphaBetaPlayer(),
    }

    log = play_match(players)

    assert log.starting_player is Player.X
    assert log.final is Outcome.DRAW
    assert log.moves == (
        Cell.TOP_LEFT,
        Cell.MIDDLE_CENTER,
        Cell.TOP_CENTER,
        Cell.TOP_RIGHT,
        Cell.BOTTOM_LEFT,
        Cell.MIDDLE_LEFT,
        Cell.MIDDLE_RIGHT,
        Cell.BOTTOM_CENTER,
        Cell.BOTTOM_RIGHT,
    )


def test_play_match_records_moves_and_outcome_with_other_player() -> None:
    players = {
        Player.X: AlphaBetaPlayer(),
        Player.O: AlphaBetaPlayer(),
    }

    log = play_match(
        players,
        initial_state=GameState(
            board=Board.empty(),
            current_player=Player.O,
        ),
    )

    assert log.starting_player is Player.O
    assert log.final is Outcome.DRAW
    assert log.moves == (
        Cell.TOP_LEFT,
        Cell.MIDDLE_CENTER,
        Cell.TOP_CENTER,
        Cell.TOP_RIGHT,
        Cell.BOTTOM_LEFT,
        Cell.MIDDLE_LEFT,
        Cell.MIDDLE_RIGHT,
        Cell.BOTTOM_CENTER,
        Cell.BOTTOM_RIGHT,
    )
