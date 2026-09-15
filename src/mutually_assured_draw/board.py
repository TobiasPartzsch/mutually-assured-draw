from dataclasses import dataclass

from .game_types import Cell, Mark, Player

WINNING_LINES = (
    (Cell.TOP_LEFT, Cell.TOP_CENTER, Cell.TOP_RIGHT),
    (Cell.MIDDLE_LEFT, Cell.MIDDLE_CENTER, Cell.MIDDLE_RIGHT),
    (Cell.BOTTOM_LEFT, Cell.BOTTOM_CENTER, Cell.BOTTOM_RIGHT),
    (Cell.TOP_LEFT, Cell.MIDDLE_LEFT, Cell.BOTTOM_LEFT),
    (Cell.TOP_CENTER, Cell.MIDDLE_CENTER, Cell.BOTTOM_CENTER),
    (Cell.TOP_RIGHT, Cell.MIDDLE_RIGHT, Cell.BOTTOM_RIGHT),
    (Cell.TOP_LEFT, Cell.MIDDLE_CENTER, Cell.BOTTOM_RIGHT),
    (Cell.TOP_RIGHT, Cell.MIDDLE_CENTER, Cell.BOTTOM_LEFT),
)


@dataclass(frozen=True)
class Board:
    cells: tuple[Mark, ...]

    @classmethod
    def empty(cls) -> "Board":
        return cls((Mark.EMPTY,) * len(Cell))

    @classmethod
    def from_string(cls, state_str: str) -> "Board":
        if len(state_str) != len(Cell):
            raise ValueError(f"State string must have length {len(Cell)}")
        try:
            return cls(tuple(Mark(c) for c in state_str))
        except ValueError as err:
            raise ValueError(f"Invalid character in state string: {err}") from err

    def cell_at(self, cell: Cell) -> Mark:
        return self.cells[cell]

    def place(self, cell: Cell, player: Player) -> "Board":
        if self.cell_at(cell) is not Mark.EMPTY:
            raise ValueError(f"Cell {cell.name} is already occupied")

        updated_cells = list(self.cells)
        updated_cells[cell] = Mark(player)
        return Board(tuple(updated_cells))

    @property
    def is_full(self) -> bool:
        return Mark.EMPTY not in self.cells

    @property
    def winner(self) -> Player | None:
        for winning_line in WINNING_LINES:
            first, second, third = (self.cell_at(cell) for cell in winning_line)
            if first == Mark.EMPTY:
                continue
            if first == second == third:
                return Player(first)
        return None

    @property
    def available_cells(self) -> list[Cell]:
        return [cell for cell in Cell if self.cell_at(cell) == Mark.EMPTY]

    def serialize(self) -> str:
        """Return a compact 9-character representation (e.g. 'XO--X--O-')."""
        return "".join(self.cells)

    def __repr__(self) -> str:
        return f"Board('{self.serialize()}')"

    def __str__(self) -> str:
        s = [c.value if c is not Mark.EMPTY else " " for c in self.cells]
        return (
            f" {s[0]} | {s[1]} | {s[2]} \n"
            f"---+---+---\n"
            f" {s[3]} | {s[4]} | {s[5]} \n"
            f"---+---+---\n"
            f" {s[6]} | {s[7]} | {s[8]} "
        )
