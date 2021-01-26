import pytest

from game.minesweeper import MinesweeperGame, MinesweeperException, VisibleCellState, MinesweeperCell, HiddenCellState, \
    MineCellState, EmptyCellState


def test_cant_create_game_with_more_mines_than_cells():
    with pytest.raises(MinesweeperException) as excinfo:
        MinesweeperGame(10, 10, 101)
    assert str(excinfo.value) == "The board can not have more mines than cells"


def test_create_game_makes_a_board_with_correct_dimensions_mine_count_and_all_cells_hidden():
    columns = 4
    rows = 10
    expected_mine_count = 5
    game = MinesweeperGame(columns, rows, expected_mine_count)
    assert len(game.board) == 4
    assert all([len(column) == 10 for column in game.board])
    assert not game.is_over

    actual_mine_count = 0
    for x_position in range(columns):
        for y_position in range(rows):
            cell = game.get_cell(x_position, y_position)
            assert cell.visible_state == HiddenCellState()
            if cell.has_mine:
                actual_mine_count += 1

    assert actual_mine_count == expected_mine_count


def test_player_starts_with_all_cells_hidden():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]

    game = MinesweeperGame.from_board(board)
    hidden = HiddenCellState()
    expected_board = [[hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden]]
    assert game.visible_board == expected_board


def test_adjacent_cells_of_each_cell_can_be_accessed():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(4)] for x_position in range(4)
    ]

    game = MinesweeperGame.from_board(board)

    cell = game.get_cell(0, 0)
    adjacent_cells = {(adj_cell.x_position, adj_cell.y_position) for adj_cell in cell.adjacent_cells}
    assert adjacent_cells == {        (1, 0),
                              (0, 1), (1, 1)}

    cell = game.get_cell(0, 1)
    adjacent_cells = {(adj_cell.x_position, adj_cell.y_position) for adj_cell in cell.adjacent_cells}
    assert adjacent_cells == {(0, 0), (1, 0),
                                      (1, 1),
                              (0, 2), (1, 2)}

    cell = game.get_cell(1, 1)
    adjacent_cells = {(adj_cell.x_position, adj_cell.y_position) for adj_cell in cell.adjacent_cells}
    assert adjacent_cells == {(0, 0), (1, 0), (2, 0),
                              (0, 1),         (2, 1),
                              (0, 2), (1, 2), (2, 2)}

    cell = game.get_cell(3, 3)
    adjacent_cells = {(adj_cell.x_position, adj_cell.y_position) for adj_cell in cell.adjacent_cells}
    assert adjacent_cells == {(2, 2), (3, 2),
                              (2, 3)         }

    cell = game.get_cell(3, 0)
    adjacent_cells = {(adj_cell.x_position, adj_cell.y_position) for adj_cell in cell.adjacent_cells}
    assert adjacent_cells == {(2, 0),
                              (2, 1), (3, 1)}

    cell = game.get_cell(1, 3)
    adjacent_cells = {(adj_cell.x_position, adj_cell.y_position) for adj_cell in cell.adjacent_cells}
    assert adjacent_cells == {(0, 2), (1, 2), (2, 2),
                              (0, 3),         (2, 3)}


def test_revealing_a_cell_with_a_mine_ends_the_game_as_looser():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]
    board[0][0].add_mine()

    game = MinesweeperGame.from_board(board)
    cell_state = game.reveal_cell_position(0, 0)
    assert isinstance(cell_state, MineCellState)
    assert game.is_over
    assert game.was_lost


def test_revealing_a_cell_without_a_mine_shows_the_number_of_mines_around_it():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]
    board[0][0].add_mine()
    board[1][0].add_mine()
    board[2][0].add_mine()
    board[0][1].add_mine()
    board[2][1].add_mine()
    board[0][2].add_mine()
    board[1][2].add_mine()
    board[2][2].add_mine()
    game = MinesweeperGame.from_board(board)

    cell_state = game.reveal_cell_position(1, 1)
    assert isinstance(cell_state, EmptyCellState)
    assert cell_state.adjacent_mines == 8

    hidden = HiddenCellState()
    empty_with_eight = EmptyCellState(8)
    expected_board = [[hidden, hidden, hidden, hidden, hidden],
                      [hidden, empty_with_eight, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden]]
    assert game.visible_board == expected_board

    assert not game.is_over


def test_revealing_a_cell_without_mines_around_it_reveals_adjacent_cells():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]
    board[2][0].add_mine()
    board[2][1].add_mine()
    board[2][2].add_mine()
    board[1][2].add_mine()
    board[0][2].add_mine()
    game = MinesweeperGame.from_board(board)

    cell_state = game.reveal_cell_position(0, 0)
    assert isinstance(cell_state, EmptyCellState)
    assert cell_state.adjacent_mines == 0

    hidden = HiddenCellState()
    expected_board = [[EmptyCellState(0), EmptyCellState(2), hidden, hidden, hidden],
                      [EmptyCellState(2), EmptyCellState(5), hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden],
                      [hidden, hidden, hidden, hidden, hidden]]
    assert game.visible_board == expected_board

    assert not game.is_over


def test_revealing_a_cell_without_mines_around_it_reveals_adjacent_cells_recursively():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]
    board[4][4].add_mine()
    game = MinesweeperGame.from_board(board)

    cell_state = game.reveal_cell_position(0, 0)
    assert isinstance(cell_state, EmptyCellState)
    assert cell_state.adjacent_mines == 0

    hidden = HiddenCellState()
    empty_with_zero = EmptyCellState(0)
    expected_board = [[empty_with_zero, empty_with_zero, empty_with_zero, empty_with_zero, empty_with_zero],
                      [empty_with_zero, empty_with_zero, empty_with_zero, empty_with_zero, empty_with_zero],
                      [empty_with_zero, empty_with_zero, empty_with_zero, empty_with_zero, empty_with_zero],
                      [empty_with_zero, empty_with_zero, empty_with_zero, EmptyCellState(1), EmptyCellState(1)],
                      [empty_with_zero, empty_with_zero, empty_with_zero, EmptyCellState(1), hidden]]
    assert game.visible_board == expected_board

    assert not game.is_over


def test_cant_reveal_cells_when_game_is_over():
    board = [
        [MinesweeperCell(x_position, y_position) for y_position in range(5)] for x_position in range(5)
    ]
    board[0][0].add_mine()

    game = MinesweeperGame.from_board(board)
    cell_state = game.reveal_cell_position(0, 0)
    assert isinstance(cell_state, MineCellState)
    assert game.is_over

    with pytest.raises(MinesweeperException) as excinfo:
        game.reveal_cell_position(1, 1)
    assert str(excinfo.value) == "Can not reveal cell, the game is over."
