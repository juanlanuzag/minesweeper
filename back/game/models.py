from django.db import models

from game.minesweeper import MinesweeperGame, MinesweeperCell


class GameQueryset(models.QuerySet):
    def create_from_minesweeper_game(self, minesweeper_game):
        return self.create(columns=minesweeper_game.columns, rows=minesweeper_game.rows,
                           mines=minesweeper_game.mines, was_lost=minesweeper_game.was_lost,
                           was_won=minesweeper_game.was_won, board=minesweeper_game.get_board_as_json())


class Game(models.Model):
    rows = models.PositiveIntegerField()
    columns = models.PositiveIntegerField()
    mines = models.PositiveIntegerField()
    was_lost = models.BooleanField(default=False)
    was_won = models.BooleanField(default=False)
    board = models.JSONField()

    objects = GameQueryset.as_manager()

    def to_minesweeper_game(self):
        board = [
            [
                MinesweeperCell(json_cell['x_position'], json_cell['y_position'],
                                json_cell['has_mine'], json_cell['is_revealed'],
                                json_cell['is_flagged']) for json_cell in column
            ] for column in self.board
        ]
        return MinesweeperGame(self.columns, self.rows, self.mines, board, self.was_won, self.was_lost)

    def update_from_minesweeper_game(self, minesweeper_game):
        self.columns = minesweeper_game.columns
        self.rows = minesweeper_game.rows
        self.mines = minesweeper_game.mines
        self.was_lost = minesweeper_game.was_lost
        self.was_won = minesweeper_game.was_won
        self.board = minesweeper_game.get_board_as_json()
        self.save()

