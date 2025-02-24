from abc import ABC, abstractmethod
from project_types import (Cell, 
                           Symbol,
                           Feedback)

class SymbolPlacer(ABC):
    @abstractmethod
    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback:
        raise NotImplementedError

class TicTacToeSymbolPlacer:
    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback:
        pass

class WildTicTacToeSymbolPlacer:
    pass

class NotaktoSymbolPlacer:
    pass

class Pick15SymbolPlacer:
    pass

class WinCondition(ABC):
    @abstractmethod
    def determine_winner(self):
        pass

class TicTacToeWinCondition:
    pass

class WildTicTacToeWinCondition:
    pass

class NotaktoWinCondition:
    pass

class Pick15WinCondition:
    pass

