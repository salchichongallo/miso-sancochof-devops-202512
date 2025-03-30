from model.db import db
from model.blacklist import Blacklist


class ResetData():
    def execute(self):
        Blacklist.query.delete()
        db.session.commit()
