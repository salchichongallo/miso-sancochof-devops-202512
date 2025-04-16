import pytest
from unittest.mock import MagicMock
from commands.verify_email import CheckEmailCommand
from model.db import db
from model.blacklist import Blacklist


@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()
    db.session = mock_session
    return mock_session


def test_execute_email_not_blacklisted(mock_db_session):
    email = "test@example.com"
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    command = CheckEmailCommand(email)

    result = command.execute()

    assert result == {
        "is_blacklisted": False,
        "reason": "Email no encontrado",
    }
    mock_db_session.query.assert_called_once_with(Blacklist)
    mock_db_session.query.return_value.filter_by.assert_called_once_with(email=email)


def test_execute_email_blacklisted(mock_db_session):
    email = "blacklisted@example.com"
    mock_blacklist_entry = MagicMock()
    mock_blacklist_entry.blocked_reason = "Spam activity"
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_blacklist_entry
    command = CheckEmailCommand(email)

    result = command.execute()

    assert result == {
        "is_blacklisted": True,
        "reason": "Spam activity",
    }
    mock_db_session.query.assert_called_once_with(Blacklist)
    mock_db_session.query.return_value.filter_by.assert_called_once_with(email=email)
