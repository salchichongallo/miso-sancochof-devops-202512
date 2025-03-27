import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()

class Model:
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   createdAt = Column(DateTime, default=datetime.now)

