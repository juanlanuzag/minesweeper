import pytest

from game.minesweeper import MinesweeperGame, MinesweeperException


def test_cant_create_game_with_more_mines_than_cells():
    with pytest.raises(MinesweeperException) as excinfo:
        MinesweeperGame(10, 10, 101)
    assert str(excinfo.value) == "The board can not have more mines than cells"


def test_create_game_makes_a_board_with_correct_dimensions_and_mine_count():
    columns = 4
    rows = 10
    expected_mine_count = 5
    game = MinesweeperGame(columns, rows, expected_mine_count)
    assert len(game.board) == 4
    assert all([len(column) == 10 for column in game.board])

    actual_mine_count = 0
    for x_position in range(columns):
        for y_position in range(rows):
            if game.get_cell(x_position, y_position).has_mine:
                actual_mine_count += 1

    assert actual_mine_count == expected_mine_count
