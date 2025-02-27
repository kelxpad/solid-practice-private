from abc import ABC, abstractmethod
from .project_types import (Cell, 
                           Symbol,
                           Feedback,
                           Field,
                           PlayerId)

class SymbolPlacer(ABC):
    @abstractmethod
    def place_symbol(self, 
                     field: Field, 
                     symbol: Symbol, 
                     cell: Cell) -> Feedback:
        pass

class TicTacToeSymbolPlacer(SymbolPlacer):
    def place_symbol(self, 
                     field: Field, 
                     symbol: Symbol, 
                     cell: Cell) -> Feedback:
        if field.get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED
        if not field.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        field.place_symbol(symbol, cell)
        return Feedback.VALID

class WildTicTacToeSymbolPlacer(SymbolPlacer):
    pass

class NotaktoSymbolPlacer:
    pass

class Pick15SymbolPlacer:
    pass

class WinCondition(ABC):
    @abstractmethod
    def check_winner(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        pass

class TicTacToeWinCondition(WinCondition):
    def check_winner(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        row_groups = [
            [Cell(row, k) for k in field.valid_coords]
            for row in field.valid_coords
        ]

        col_groups = [
            [Cell(k, col) for k in field.valid_coords]
            for col in field.valid_coords
        ]

        diagonals = [
            # Backslash
            [Cell(k, k) for k in field.valid_coords],
            # Forward slash
            [Cell(k, field.grid_size - k + 1)
             for k in field.valid_coords],
        ]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and \
                        field.are_all_equal_to_basis(basis, group):
                    winner = symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'

                    return winner

        return None

class WildTicTacToeWinCondition(WinCondition):
    def check_winner(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]) -> PlayerId | None:
        row_groups = [
            [Cell(row, k) for k in field.valid_coords]
            for row in field.valid_coords
        ]

        col_groups = [
            [Cell(k, col) for k in field.valid_coords]
            for col in field.valid_coords
        ]

        diagonals = [
            [Cell(k, k) for k in field.valid_coords],  # Backslash
            [Cell(k, field.grid_size - k + 1) for k in field.valid_coords],  # Forward slash
        ]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and \
                        field.are_all_equal_to_basis(basis, group):
                    
                    # Retrieve the PlayerId associated with the winning symbol
                    winner = symbol_to_player.get(basis)
                    
                    assert winner is not None, f'Winning symbol {basis} has no associated player'
                    
                    return winner

        return None

class NotaktoWinCondition:
    pass

class Pick15WinCondition:
    pass