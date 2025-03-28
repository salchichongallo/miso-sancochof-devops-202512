from sqlalchemy.exc import IntegrityError
from ..model.db import db
from ..model.blacklist import Blacklist
from ..errors.errors import DuplicatedEmailError


class BlockEmailCommand:
    def __init__(self, email, app_uuid, blocked_reason=None):
        self.email = email
        self.app_uuid = app_uuid
        self.blocked_reason = blocked_reason

    def execute(self):
        blacklist = Blacklist(
            email=self.email,
            app_uuid=self.app_uuid,
            blocked_reason=self.blocked_reason,
            ip='127.0.0.1',  # TODO: Get the IP
        )
        db.session.add(blacklist)
        try:
            db.session.commit()
        except IntegrityError:
            raise DuplicatedEmailError()
        return {
            'id': str(blacklist.id),
            'email': blacklist.email,
            'app_uuid': blacklist.app_uuid,
            'blocked_reason': blacklist.blocked_reason,
            'ip': blacklist.ip,
            'created_at': blacklist.createdAt.isoformat(),
        }
