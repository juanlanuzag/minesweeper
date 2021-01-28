import pytest
from rest_framework import status
from rest_framework.test import APIClient


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
