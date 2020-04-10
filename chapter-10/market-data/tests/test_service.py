import pytest
from service import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client


def test_index(client):
    rv = client.get('/ping')
    assert rv.status == '200 OK'
