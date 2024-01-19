import uuid
from db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4(), server_default=uuid.uuid4().hex
    )
    phone: Mapped[str] = mapped_column(String(11), unique=True, index=True)
    password: Mapped[str]
