import pytest
from unittest.mock import patch
from flask import Flask
from blueprints.reset import reset_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(reset_bp)
    app.testing = True
    with app.test_client() as client:
        yield client


@patch('commands.reset_data.ResetData.execute')
def test_reset_success(mock_execute, client):
    mock_execute.return_value = None

    response = client.delete('/reset')

    assert response.status_code == 200
    assert response.json == {'message': 'Todos los datos han sido borrados'}

    mock_execute.assert_called_once()
