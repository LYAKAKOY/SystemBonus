import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from api.handlers.users.schemas import CreatedUser, UpdatedUser
from db.users.dals import UserDAL
from hashing import Hasher


async def _create_user(phone: str, password: str, session: AsyncSession) -> CreatedUser | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(phone=phone, password=Hasher.get_password_hash(password))
        if user:
            return CreatedUser(user_id=user.user_id)


async def _update_user(user_id: uuid.UUID, is_active: bool, is_verified_phone: bool, session: AsyncSession) -> UpdatedUser | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user_id = await user_dal.update_user(user_id=user_id, is_active=is_active, is_verified_phone=is_verified_phone)
        if user_id:
            return UpdatedUser(user_id=user_id)
