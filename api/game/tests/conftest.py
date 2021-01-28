import pytest

from game.minesweeper import MinesweeperCell


@pytest.fixture
def board_5_by_5():
    return [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]
