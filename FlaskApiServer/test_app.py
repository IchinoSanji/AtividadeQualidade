import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_items_empty(client):
    rv = client.get('/items')
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_post_item(client):
    rv = client.post('/items', json={'name': 'item1'})
    assert rv.status_code == 201
    assert rv.get_json()['message'] == 'Item added'

def test_post_invalid_item(client):
    rv = client.post('/items', json={})
    assert rv.status_code == 400
    assert 'error' in rv.get_json()