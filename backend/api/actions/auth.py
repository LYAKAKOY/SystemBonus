import uuid
from api.handlers.schemas import CreatedUser
from db.users.models import User
from db.users.user_dal import UserDAL
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def _get_user_by_user_id_for_auth(
        user_id: uuid.UUID, session: AsyncSession
) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_user_id(user_id=user_id)


async def _get_user_by_login_for_auth(phone: str, session: AsyncSession) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_phone(phone=phone)


async def authenticate_user(phone: str, password: str, db: AsyncSession) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if (user := await _get_user_by_login_for_auth(phone=phone, session=db)) is None:
        raise credentials_exception
    if not Hasher.verify_password(password, user.password):
        raise credentials_exception
    return user


async def _create_user(phone: str, password: str, session: AsyncSession) -> CreatedUser | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(phone=phone, password=Hasher.get_password_hash(password))
        if user:
            return CreatedUser(user_id=user.user_id)
