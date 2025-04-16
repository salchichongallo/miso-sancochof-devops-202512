import pytest
from unittest.mock import MagicMock, patch
from commands.reset_data import ResetData


@pytest.fixture
def reset_data_instance():
    return ResetData()


@patch('commands.reset_data.Blacklist')
@patch('commands.reset_data.db')
def test_execute_calls_delete_and_commit(mock_db, mock_blacklist, reset_data_instance):
    mock_blacklist.query.delete = MagicMock()
    mock_db.session.commit = MagicMock()

    reset_data_instance.execute()

    mock_blacklist.query.delete.assert_called_once()
    mock_db.session.commit.assert_called_once()


@patch('commands.reset_data.Blacklist')
@patch('commands.reset_data.db')
def test_execute_handles_exceptions(mock_db, mock_blacklist, reset_data_instance):
    mock_blacklist.query.delete = MagicMock(side_effect=Exception("Delete failed"))
    mock_db.session.commit = MagicMock()

    with pytest.raises(Exception, match="Delete failed"):
        reset_data_instance.execute()

    mock_blacklist.query.delete.assert_called_once()
    mock_db.session.commit.assert_not_called()
