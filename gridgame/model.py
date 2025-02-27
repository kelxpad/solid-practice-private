from collections.abc import Sequence
from .variants import (SymbolPlacer,
                       WinCondition
                       )
from .project_types import (PlayerId, 
                            Cell, 
                            Symbol, 
                            Feedback, 
                            Field)

class GridGameModel:
    def __init__(self, 
                 grid_size: int, 
                 player_symbols: Sequence[Symbol], 
                 player_count: int,
                 symbol_placer: SymbolPlacer,
                 win_condition: WinCondition):
        if player_count <= 1:
            raise ValueError(
                f'Must have at least two players (found {player_count})')

        unique_symbols = set(player_symbols)

        if len(unique_symbols) != len(player_symbols):
            raise ValueError(
                f'Player symbols must be unique (was {player_symbols}')

        if len(player_symbols) != player_count:
            raise ValueError(
                f'Player symbols must be exactly {player_count} (was {player_symbols})')

        self._field = Field(grid_size)

        self._player_count = player_count
        self._player_to_symbol: dict[PlayerId, Symbol] = {
            k: symbol
            for k, symbol in enumerate(player_symbols, start=1)
        }
        self._symbol_to_player: dict[Symbol, PlayerId] = {
            symbol: k
            for k, symbol in self._player_to_symbol.items()
        }
        self._current_player: PlayerId = 1
        self._symbol_placer = symbol_placer
        self._win_condition = win_condition

    @property
    def occupied_cells(self) -> dict[Cell, Symbol]:
        return self._field.occupied_cells

    @property
    def grid_size(self):
        return self._field.grid_size

    @property
    def is_game_over(self):
        return (
            self.winner is not None or
            not self._field.has_unoccupied_cell()
        )

    @property
    def current_player(self) -> PlayerId:
        return self._current_player

    @property
    def player_count(self):
        return self._player_count

    @property
    def next_player(self) -> PlayerId:
        return (
            self.current_player + 1 if self.current_player != self.player_count else
            1
        )

    @property
    def winner(self) -> PlayerId | None:
        return self._win_condition.check_winner(self._field)
    

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        if player not in self._player_to_symbol:
            raise ValueError(f'Invalid player: {player}')

        return [self._player_to_symbol[player]]

    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback: # put this part sa tictactoesymbolplacer
        result = self._symbol_placer.place_symbol(self._field, symbol, cell)
        if result == Feedback.VALID:
            self._switch_to_next_player()
        return result

    def _switch_to_next_player(self):
        self._current_player = self.next_player
