import pytest
from flask import Flask
from blueprints.ping import ping_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(ping_bp)
    with app.test_client() as client:
        yield client


def test_ping_route(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.data.decode() == "pong"
