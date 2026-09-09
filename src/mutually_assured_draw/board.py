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

    def cell_at(self, cell: Cell) -> Mark:
        return self.cells[cell]

    def place(self, cell: Cell, player: Player) -> "Board":
        if self.cell_at(cell) is not Mark.EMPTY:
            raise ValueError(f"Cell {cell.name} is already occupied")

        updated_cells = list(self.cells)
        updated_cells[cell] = Mark(player)
        return Board(tuple(updated_cells))

    def is_full(self) -> bool:
        return Mark.EMPTY not in self.cells

    def winner(self) -> Player | None:
        for winning_line in WINNING_LINES:
            first, second, third = (self.cell_at(cell) for cell in winning_line)
            if first == Mark.EMPTY:
                continue
            if first == second == third:
                return Player(first)
        return None
