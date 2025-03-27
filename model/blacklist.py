from  sqlalchemy  import  Column, String
from .model import Model, Base
from sqlalchemy.dialects.postgresql import UUID


class Blacklist(Model, Base):
    __tablename__ = 'blacklists'

    email = Column(String, nullable=False, unique=True)
    app_uuid = Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = Column(String)
    ip = Column(String, nullable=False)
