import random


class MinesweeperException(Exception):
    pass


class MinesweeperGame:
    def __init__(self, columns: int, rows: int, mines: int):
        if mines > rows * columns:
            raise MinesweeperException("The board can not have more mines than cells")

        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.board = self._create_board()

    def get_cell(self, x_position: int, y_position: int):
        return self.board[x_position][y_position]

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
        mine_positions = [(random.randrange(0, self.columns), random.randrange(0, self.rows)) for i in range(self.mines)]
        for x_position, y_position in mine_positions:
            board[x_position][y_position].add_mine()
        return board


class MinesweeperCell:
    def __init__(self, x_position: int, y_position: int):
        self.x_position = x_position
        self.y_position = y_position
        self.has_mine = False

    def add_mine(self):
        self.has_mine = True

