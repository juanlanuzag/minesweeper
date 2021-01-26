import itertools
import random


class MinesweeperException(Exception):
    pass


class MinesweeperGame:
    def __init__(self, columns: int, rows: int, mines: int, board=None):
        if mines > rows * columns:
            raise MinesweeperException("The board can not have more mines than cells")

        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.was_lost = False
        self.was_won = False
        if board:
            self.board = board
        else:
            self.board = self._create_board()
        self._set_adjacent_cells()

    @property
    def is_over(self):
        return self.was_won or self.was_lost

    @classmethod
    def from_board(cls, board):
        columns = len(board)
        rows = len(board[0])
        mines = cls.get_mine_count(board)
        return cls(columns, rows, mines, board)

    @staticmethod
    def get_mine_count(board):
        columns = len(board)
        rows = len(board[0])
        mines = 0
        for x_position in range(columns):
            for y_position in range(rows):
                if board[x_position][y_position].has_mine:
                    mines += 1
        return mines

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
        self.set_if_game_won()

    def _reveal_cell(self, cell):
        if cell.is_revealed:
            # recursive call
            return

        visible_state = cell.reveal()
        if isinstance(visible_state, MineCellState):
            self.was_lost = True
        elif isinstance(visible_state, EmptyCellState) and visible_state.adjacent_mines == 0:
            for adj_cell in cell.adjacent_cells:
                self._reveal_cell(adj_cell)
        self.set_if_game_won()
        return visible_state

    def set_if_game_won(self):
        """
        The game was won it visible boards only has empty cells and flags,
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

    def _create_board(self):
        """
        Positions in the board look like:
        (0,0)  (1,0) (2,0)
        (0,1)  (1,1) (2,1)
        (0,2)  (1,2) (2,2)
        """
        board = [
            [MinesweeperCell(x_position, y_position) for y_position in range(self.rows)]
            for x_position in range(self.columns)
        ]
        mine_positions = random.sample(list(itertools.product(range(self.columns), range(self.rows))), k=self.mines)

        for x_position, y_position in mine_positions:
            board[x_position][y_position].add_mine()
        return board

    def _set_adjacent_cells(self):
        for x_position in range(self.columns):
            for y_position in range(self.rows):
                cell = self.get_cell(x_position, y_position)
                cell.set_adjacent_cells(self.get_adjacent_cells(cell))

    def get_adjacent_cells(self, cell):
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
    def __init__(self, x_position: int, y_position: int):
        self.x_position = x_position
        self.y_position = y_position
        self.has_mine = False
        self.is_revealed = False
        self.adjacent_cells = []
        self.is_flagged = False

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
        """
        State of the cell that the player sees
        """
        if self.is_revealed:
            if self.has_mine:
                return MineCellState()
            return EmptyCellState(self._adjacents_mine_count)
        if self.is_flagged:
            return FlaggedCellState()
        return HiddenCellState()
