import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from blueprints.blacklists import blacklist_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(blacklist_bp)
    app.testing = True
    with app.test_client() as client:
        yield client


@patch('blueprints.blacklists.CheckTokenCommand.execute')
@patch('blueprints.blacklists.NewBlacklistJsonSchema.check')
@patch('blueprints.blacklists.BlockEmailCommand')
def test_add_email(mock_block_email_command, mock_new_blacklist_json_schema, mock_check_token, client):
    mock_check_token.return_value = None
    mock_new_blacklist_json_schema.return_value = None
    mock_block_email_instance = MagicMock()
    mock_block_email_instance.execute.return_value = {'email': 'test@example.com'}
    mock_block_email_command.return_value = mock_block_email_instance

    response = client.post('/blacklists', json={
        'email': 'test@example.com',
        'app_uuid': '1234',
        'blocked_reason': 'spam'
    })

    assert response.status_code == 200
    assert response.json == {
        'message': 'Cuenta creada exitosamente.',
        'data': {'email': 'test@example.com'}
    }
    mock_check_token.assert_called_once()
    mock_new_blacklist_json_schema.assert_called_once_with({
        'email': 'test@example.com',
        'app_uuid': '1234',
        'blocked_reason': 'spam'
    })
    mock_block_email_command.assert_called_once_with(
        email='test@example.com',
        app_uuid='1234',
        ip='127.0.0.1',
        blocked_reason='spam'
    )
    mock_block_email_instance.execute.assert_called_once()


@patch('blueprints.blacklists.CheckTokenCommand.execute')
@patch('blueprints.blacklists.ValidateEmailJsonSchema.check')
@patch('blueprints.blacklists.CheckEmailCommand')
def test_check_blacklist(mock_check_email_command, mock_validate_email_json_schema, mock_check_token, client):
    mock_check_token.return_value = None
    mock_validate_email_json_schema.return_value = None
    mock_check_email_instance = MagicMock()
    mock_check_email_instance.execute.return_value = {'is_blacklisted': True}
    mock_check_email_command.return_value = mock_check_email_instance

    response = client.get('/blacklists/test@example.com')

    assert response.status_code == 200
    assert response.json == {'is_blacklisted': True}
    mock_check_token.assert_called_once()
    mock_validate_email_json_schema.assert_called_once_with({'email': 'test@example.com'})
    mock_check_email_command.assert_called_once_with('test@example.com')
    mock_check_email_instance.execute.assert_called_once()
