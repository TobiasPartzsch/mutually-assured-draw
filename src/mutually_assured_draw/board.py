from dataclasses import dataclass

from .game_types import Cell, Mark, Player


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
