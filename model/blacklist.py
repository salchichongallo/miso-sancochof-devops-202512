from  sqlalchemy  import  Column, String
from .model import Model, Base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields, validate, ValidationError
from ..errors.errors import ParamError


class Blacklist(Model, Base):
    __tablename__ = 'blacklists'

    email = Column(String, nullable=False, unique=True)
    app_uuid = Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = Column(String)
    ip = Column(String, nullable=False)


class NewBlacklistJsonSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))

    @staticmethod
    def check(json):
        try:
            NewBlacklistJsonSchema().load(json)
        except ValidationError as exception:
            raise ParamError.first_from(exception.messages)
