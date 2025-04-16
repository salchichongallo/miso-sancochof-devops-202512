import os
import pytest
from unittest.mock import patch
from flask import Flask
from commands.check_token import CheckTokenCommand
from errors.errors import ApiError, TokenNotProvidedError, InvalidTokenError


app = Flask(__name__)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_execute_no_auth_header():
    with app.test_request_context(headers={}):
        with pytest.raises(TokenNotProvidedError):
            CheckTokenCommand.execute()


@patch('commands.check_token.CheckTokenCommand.get_app_token')
def test_execute_invalid_token(mock_get_app_token):
    mock_get_app_token.return_value = 'valid_token'
    with app.test_request_context(headers={'Authorization': 'Bearer invalid_token'}):
        with pytest.raises(InvalidTokenError):
            CheckTokenCommand.execute()


@patch('commands.check_token.CheckTokenCommand.get_app_token')
def test_execute_valid_token(mock_get_app_token):
    mock_get_app_token.return_value = 'valid_token'
    with app.test_request_context(headers={'Authorization': 'Bearer valid_token'}):
        try:
            CheckTokenCommand.execute()
        except Exception as error:
            pytest.fail(f"Unexpected exception raised: {error}")


@patch.dict(os.environ, {}, clear=True)
def test_get_app_token_not_set():
    with pytest.raises(ApiError) as exc_info:
        CheckTokenCommand.get_app_token()
    assert exc_info.value.code == 500
    assert exc_info.value.description == 'SECRET_TOKEN not set in environment variables.'


@patch.dict(os.environ, {'SECRET_TOKEN': 'valid_token'})
def test_get_app_token_set():
    token = CheckTokenCommand.get_app_token()
    assert token == 'valid_token'
