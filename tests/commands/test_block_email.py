import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from commands.block_email import BlockEmailCommand
from errors.errors import DuplicatedEmailError


def test_blocks_the_given_email_successfully(mocker):
    mocker.patch('model.db.db.session.add', side_effect=lambda obj: setattr(obj, 'createdAt', datetime.now()))
    commit_mock = mocker.patch('model.db.db.session.commit')
    block_email = BlockEmailCommand(
        email="foo@bar.com",
        app_uuid="bar_uuid",
        ip="localhost",
        blocked_reason=None,
    )
    result = block_email.execute()
    assert result['email'] == 'foo@bar.com'
    assert result['app_uuid'] == 'bar_uuid'
    assert result['ip'] == 'localhost'
    commit_mock.assert_called()


def test_block_reason_is_none_by_default(mocker):
    mocker.patch('model.db.db.session.add', side_effect=lambda obj: setattr(obj, 'createdAt', datetime.now()))
    commit_mock = mocker.patch('model.db.db.session.commit')
    block_email = BlockEmailCommand(
        email='bar@baz.com',
        app_uuid='baz_uuid',
        ip='localhost',
    )
    result = block_email.execute()
    assert result['blocked_reason'] is None
    commit_mock.assert_called()


def test_block_email_with_the_given_reason(mocker):
    mocker.patch('model.db.db.session.add', side_effect=lambda obj: setattr(obj, 'createdAt', datetime.now()))
    commit_mock = mocker.patch('model.db.db.session.commit')
    block_email = BlockEmailCommand(
        blocked_reason='test reason',
        email='bar@baz.com',
        app_uuid='baz_uuid',
        ip='localhost',
    )
    result = block_email.execute()
    assert result['blocked_reason'] == 'test reason'
    commit_mock.assert_called()


def test_block_email_with_an_existing_email(mocker):
    mocker.patch('model.db.db.session.add')
    mocker.patch('model.db.db.session.commit', side_effect=IntegrityError(None, None, None))
    block_email = BlockEmailCommand(
        email='test@test.com',
        app_uuid='baz_uuid',
        ip='localhost',
    )
    with pytest.raises(DuplicatedEmailError):
        block_email.execute()
