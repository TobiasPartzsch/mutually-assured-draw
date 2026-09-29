from dataclasses import dataclass
from enum import StrEnum

from mutually_assured_draw.arena import play_match
from mutually_assured_draw.game_types import Outcome, Player

from .players import PlayerInterface


@dataclass(frozen=True, slots=True)
class Participant:
    name: str
    agent: PlayerInterface


class HeadToHeadOutcome(StrEnum):
    FIRST_WIN = "FIRST_WIN"
    SECOND_WIN = "SECOND_WIN"
    DRAW = "DRAW"


@dataclass(slots=True)
class HeadToHeadResult:
    first: str
    second: str
    first_wins: int
    second_wins: int
    draws: int

    def record(self, outcome: HeadToHeadOutcome) -> None:
        match outcome:
            case HeadToHeadOutcome.FIRST_WIN:
                self.first_wins += 1
            case HeadToHeadOutcome.SECOND_WIN:
                self.second_wins += 1
            case HeadToHeadOutcome.DRAW:
                self.draws += 1


def play_head_to_head(
    first: Participant,
    second: Participant,
    games_per_side: int,
) -> HeadToHeadResult:
    result = HeadToHeadResult(first.name, second.name, 0, 0, 0)
    for _ in range(games_per_side):
        match_log = play_match(players={Player.X: first.agent, Player.O: second.agent})
        result.record(result_for(match_log.final, first, first))
    for _ in range(games_per_side):
        match_log = play_match(players={Player.X: second.agent, Player.O: first.agent})
        result.record(result_for(match_log.final, first, second))
    return result


def result_for(
    outcome: Outcome,
    x_participant: Participant,
    first: Participant,
) -> HeadToHeadOutcome:
    match outcome:
        case Outcome.DRAW:
            return HeadToHeadOutcome.DRAW
        case Outcome.X_WINS:
            return (
                HeadToHeadOutcome.FIRST_WIN
                if x_participant == first
                else HeadToHeadOutcome.SECOND_WIN
            )
        case Outcome.O_WINS:
            return (
                HeadToHeadOutcome.SECOND_WIN
                if x_participant == first
                else HeadToHeadOutcome.FIRST_WIN
            )
        case Outcome.IN_PROGRESS:
            raise ValueError("A completed match cannot be in progress")
