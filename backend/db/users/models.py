import uuid
from db.base import Base
from sqlalchemy import String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column


class User(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4(), server_default=uuid.uuid4().hex
    )
    phone: Mapped[str] = mapped_column(String(11), unique=True, index=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified_phone: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")


class Profile(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), unique=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(40))
    bonuses: Mapped[int] = mapped_column(BigInteger, default=0)

    user: Mapped[User] = relationship(User, back_populates="profile")

