import itertools
import random


class MinesweeperException(Exception):
    pass


class MinesweeperGame:
    def __init__(self, columns: int, rows: int, mines: int, board, was_won=False, was_lost=False):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.was_won = was_won
        self.was_lost = was_lost
        self.board = board
        self._set_adjacent_cells()

    @classmethod
    def new_game(cls, columns, rows, mines):
        cls._validate_dimensions(columns, rows, mines)
        board = cls._create_board(columns, rows, mines)
        return cls(columns, rows, mines, board)

    @classmethod
    def from_board(cls, board):
        columns = len(board)
        rows = len(board[0])
        mines = cls._get_mine_count(board)
        return cls(columns, rows, mines, board)

    @classmethod
    def _validate_dimensions(cls, columns, rows, mines):
        if mines > rows * columns:
            raise MinesweeperException("The board can not have more mines than cells")

    @classmethod
    def _create_board(cls, columns, rows, mines):
        """
        Positions in the board look like:
        (0,0)  (1,0) (2,0)
        (0,1)  (1,1) (2,1)
        (0,2)  (1,2) (2,2)
        """
        board = [
            [MinesweeperCell(x_position, y_position) for y_position in range(rows)]
            for x_position in range(columns)
        ]
        mine_positions = random.sample(list(itertools.product(range(columns), range(rows))), k=mines)

        for x_position, y_position in mine_positions:
            board[x_position][y_position].add_mine()
        return board

    @property
    def is_over(self):
        return self.was_won or self.was_lost

    def get_cell(self, x_position: int, y_position: int):
        return self.board[x_position][y_position]

    @property
    def visible_board(self):
        return [
            [self.get_cell(x_position, y_position).visible_state for y_position in range(self.rows)]
            for x_position in range(self.columns)
        ]

    def reveal_cell_position(self, x_position: int, y_position: int):
        if self.is_over:
            raise MinesweeperException("Can not reveal cell, the game is over.")
        cell = self.get_cell(x_position, y_position)
        return self._reveal_cell(cell)

    def set_flag_on_cell_position(self, x_position: int, y_position: int, is_flagged: bool):
        if self.is_over:
            raise MinesweeperException("Cant set flag on cell, the game is over.")
        cell = self.get_cell(x_position, y_position)
        cell.set_flag(is_flagged)
        self._set_if_game_won()

    @staticmethod
    def _get_mine_count(board):
        columns = len(board)
        rows = len(board[0])
        mines = 0
        for x_position in range(columns):
            for y_position in range(rows):
                if board[x_position][y_position].has_mine:
                    mines += 1
        return mines

    def get_board_as_json(self):
        return [
            [self.get_cell(x_position, y_position).as_json() for y_position in range(self.rows)]
            for x_position in range(self.columns)
        ]

    @staticmethod
    def get_visible_board_state(json_board):
        return [
            [
                str(MinesweeperCell.get_visible_state(
                    cell['is_revealed'], cell['has_mine'],
                    cell['is_flagged'], cell['adjacent_mine_count']))
                for cell in column
            ]
            for column in json_board
        ]

    def _reveal_cell(self, cell):
        visible_state = cell.reveal()
        if isinstance(visible_state, MineCellState):
            self.was_lost = True
        elif isinstance(visible_state, EmptyCellState) and visible_state.adjacent_mines == 0:
            for adj_cell in cell.adjacent_cells:
                if not adj_cell.is_revealed:
                    self._reveal_cell(adj_cell)
        self._set_if_game_won()
        return visible_state

    def _set_if_game_won(self):
        """
        The game was won if visible boards only has empty cells and flags,
        and the number of flags equals the number of mines
        """
        flag_count = 0
        for x_position in range(self.columns):
            for y_position in range(self.rows):
                visible_state = self.get_cell(x_position, y_position).visible_state
                if not isinstance(visible_state, EmptyCellState) and not isinstance(visible_state, FlaggedCellState):
                    return
                if isinstance(visible_state, FlaggedCellState):
                    flag_count += 1
        if flag_count == self.mines:
            self.was_won = True

    def _set_adjacent_cells(self):
        for x_position in range(self.columns):
            for y_position in range(self.rows):
                cell = self.get_cell(x_position, y_position)
                cell.set_adjacent_cells(self._get_adjacent_cells(cell))

    def _get_adjacent_cells(self, cell):
        x_position = cell.x_position
        y_position = cell.y_position
        return {self.get_cell(x, y)
                for x in range(max(x_position-1, 0), min(x_position+2, self.columns))
                for y in range(max(y_position-1, 0), min(y_position+2, self.rows))
                if (x, y) != (x_position, y_position)}


class VisibleCellState:
    pass


class HiddenCellState(VisibleCellState):
    def __eq__(self, other):
        return isinstance(other, HiddenCellState)

    def __repr__(self):
        return 'hidden'


class FlaggedCellState(VisibleCellState):
    def __eq__(self, other):
        return isinstance(other, FlaggedCellState)

    def __repr__(self):
        return 'flag'


class MineCellState(VisibleCellState):
    def __eq__(self, other):
        return isinstance(other, MineCellState)

    def __repr__(self):
        return 'mine'


class EmptyCellState(VisibleCellState):
    def __init__(self, adjacent_mines: int):
        self.adjacent_mines = adjacent_mines
        super().__init__()

    def __repr__(self):
        return str(self.adjacent_mines)

    def __eq__(self, other):
        return isinstance(other, EmptyCellState) and self.adjacent_mines == other.adjacent_mines


class MinesweeperCell:
    def __init__(self, x_position: int, y_position: int, has_mine=False, is_revealed=False, is_flagged=False):
        self.x_position = x_position
        self.y_position = y_position
        self.has_mine = has_mine
        self.is_revealed = is_revealed
        self.is_flagged = is_flagged
        self.adjacent_cells = []

    def add_mine(self):
        self.has_mine = True

    def set_adjacent_cells(self, cells):
        self.adjacent_cells = cells

    @property
    def _adjacents_mine_count(self):
        mine_count = 0
        for cell in self.adjacent_cells:
            if cell.has_mine:
                mine_count += 1
        return mine_count

    def reveal(self):
        if self.is_flagged:
            raise MinesweeperException("Can not reveal cell, it is flagged.")
        self.is_revealed = True
        return self.visible_state

    def set_flag(self, is_flagged: bool):
        if self.is_revealed:
            raise MinesweeperException("Cant set flag on cell, the cell is already revealed.")
        self.is_flagged = is_flagged

    @property
    def visible_state(self):
        return self.get_visible_state(self.is_revealed, self.has_mine,
                                      self.is_flagged, self._adjacents_mine_count)

    @staticmethod
    def get_visible_state(is_revealed, has_mine, is_flagged, adjacent_mine_count):
        """
        State of the cell that the player sees
        """
        if is_revealed:
            if has_mine:
                return MineCellState()
            return EmptyCellState(adjacent_mine_count)
        if is_flagged:
            return FlaggedCellState()
        return HiddenCellState()

    def as_json(self):
        return {
            'x_position': self.x_position,
            'y_position': self.y_position,
            'has_mine': self.has_mine,
            'is_revealed': self.is_revealed,
            'is_flagged': self.is_flagged,
            'adjacent_mine_count': self._adjacents_mine_count
        }
