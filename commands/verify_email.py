from model.db import db
from model.blacklist import Blacklist

class CheckEmailCommand:
    def __init__(self, email):
        self.email = email

    def execute(self):
        exist = db.session.query(Blacklist).filter_by(email=self.email).first()
        return {
                "is_blacklisted": True if exist else False,
                "reason": exist.blocked_reason if exist else "Email no encontrado",
            }
