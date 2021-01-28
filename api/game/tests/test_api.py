import pytest
from rest_framework import status
from rest_framework.test import APIClient

from game.minesweeper import MinesweeperGame
from game.models import Game


def assert_starting_game_status(data):
    assert data['rows'] == 10
    assert data['columns'] == 10
    assert data['mines'] == 10
    assert not data['was_lost']
    assert not data['was_won']
    assert not data['is_over']
    cells = [cell for column in data['board'] for cell in column]
    assert len(data['board']) == 10
    assert len(data['board'][0]) == 10
    assert len(cells) == 100
    assert all(cell == 'hidden' for cell in cells)
    assert 'id' in data


@pytest.mark.django_db
def test_create_new_minesweeper_game_returns_the_game_status_with_the_game_id():
    client = APIClient()
    response = client.post('/api/minesweeper/', {'rows': 10, 'columns': 10, 'mines': 10}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert_starting_game_status(response.data)
    assert response.data['id'] == 1


@pytest.mark.django_db
def test_retreive_minesweeper_finds_the_game_by_id_and_returns_its_complete_status():
    client = APIClient()
    response = client.post('/api/minesweeper/', {'rows': 10, 'columns': 10, 'mines': 10}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    game_id = response.data['id']
    response = client.get(f'/api/minesweeper/{game_id}/', format='json')
    assert response.status_code == status.HTTP_200_OK
    assert_starting_game_status(response.data)


@pytest.mark.django_db
def test_list_minesweeper_returns_all_games():
    client = APIClient()
    # Create 11 games
    for _ in range(11):
        response = client.post('/api/minesweeper/', {'rows': 10, 'columns': 10, 'mines': 10}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    response = client.get(f'/api/minesweeper/', format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 11
    for game in response.data:
        assert_starting_game_status(game)


@pytest.mark.django_db
def test_flag_cell_returns_updated_game_with_a_flag_on_the_cell():
    client = APIClient()
    response = client.post('/api/minesweeper/', {'rows': 5, 'columns': 5, 'mines': 5}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    game_id = response.data['id']
    response = client.post(f'/api/minesweeper/{game_id}/flag_cell/',
                           data={'x_position': 0, 'y_position': 0, 'is_flagged': True}, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['rows'] == 5
    assert response.data['columns'] == 5
    assert response.data['mines'] == 5
    assert not response.data['was_lost']
    assert not response.data['was_won']
    assert not response.data['is_over']
    cells = [cell for column in response.data['board'] for cell in column]
    assert len(response.data['board']) == 5
    assert len(response.data['board'][0]) == 5
    assert len(cells) == 25
    assert cells[0] == 'flag'
    assert all(cell == 'hidden' for cell in cells[1:])


@pytest.mark.django_db
def test_reveal_cell_returns_updated_game(board_5_by_5):
    """
    Since board has no mine, revealing one cell wins the game
    """
    minesweeper_game = MinesweeperGame.from_board(board_5_by_5)
    game = Game.objects.create_from_minesweeper_game(minesweeper_game)

    client = APIClient()
    response = client.post(f'/api/minesweeper/{game.id}/reveal_cell/',
                           data={'x_position': 0, 'y_position': 0}, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['rows'] == 5
    assert response.data['columns'] == 5
    assert response.data['mines'] == 0
    assert not response.data['was_lost']
    assert response.data['was_won']
    assert response.data['is_over']
    cells = [cell for column in response.data['board'] for cell in column]
    assert len(response.data['board']) == 5
    assert len(response.data['board'][0]) == 5
    assert len(cells) == 25
    assert all(cell == '0' for cell in cells[1:])


@pytest.mark.django_db
def test_cant_flag_cell_if_game_is_over():
    client = APIClient()
    response = client.post('/api/minesweeper/', {'rows': 5, 'columns': 5, 'mines': 25}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    game_id = response.data['id']
    response = client.post(f'/api/minesweeper/{game_id}/reveal_cell/',
                           data={'x_position': 0, 'y_position': 0}, format='json')
    # Since all cells have mines, we already lost
    assert response.status_code == status.HTTP_200_OK
    assert response.data['was_lost']
    assert not response.data['was_won']
    assert response.data['is_over']

    response = client.post(f'/api/minesweeper/{game_id}/flag_cell/',
                           data={'x_position': 1, 'y_position': 1, 'is_flagged': True}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == 'Cant set flag on cell, the game is over.'


@pytest.mark.django_db
def test_cant_reveal_cell_if_game_is_over():
    client = APIClient()
    response = client.post('/api/minesweeper/', {'rows': 5, 'columns': 5, 'mines': 25}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    game_id = response.data['id']
    response = client.post(f'/api/minesweeper/{game_id}/reveal_cell/',
                           data={'x_position': 0, 'y_position': 0}, format='json')
    # Since all cells have mines, we already lost
    assert response.status_code == status.HTTP_200_OK
    assert response.data['was_lost']
    assert not response.data['was_won']
    assert response.data['is_over']

    response = client.post(f'/api/minesweeper/{game_id}/reveal_cell/',
                           data={'x_position': 1, 'y_position': 1}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == 'Can not reveal cell, the game is over.'
