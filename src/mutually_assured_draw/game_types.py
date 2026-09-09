from enum import IntEnum, StrEnum


class Player(StrEnum):
    X = "X"
    O = "O"


class Mark(StrEnum):
    EMPTY = " "
    X = "X"
    O = "O"


class Cell(IntEnum):
    TOP_LEFT = 0
    TOP_CENTER = 1
    TOP_RIGHT = 2
    MIDDLE_LEFT = 3
    MIDDLE_CENTER = 4
    MIDDLE_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_CENTER = 7
    BOTTOM_RIGHT = 8
