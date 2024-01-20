import json
import random
import uuid

import aiohttp
from aiohttp.web_response import Response

import settings
from api.handlers.users.schemas import ShowUser
from db.session import get_db
from db.users.models import User
from db.users.dals import UserDAL
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jwt_auth import JWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def generate_code() -> str:
    confirmation_code = "".join(random.choice("0123456789") for _ in range(4))
    return confirmation_code


async def _get_user_by_user_id_for_auth(
        user_id: uuid.UUID, session: AsyncSession
) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_user_id(user_id=user_id)


async def _get_user_by_phone_for_auth(phone: str, session: AsyncSession) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_phone(phone=phone)


async def authenticate_user(phone: str, password: str, db: AsyncSession) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if (user := await _get_user_by_phone_for_auth(phone=phone, session=db)) is None:
        raise credentials_exception
    if not Hasher.verify_password(password, user.password):
        raise credentials_exception
    return user


async def send_message_to_whatsapp(phone: str, message: str) -> Response:
    data = json.dumps(
        {
            "to": f"{phone}@s.whatsapp.net",
            "ephemeral": 900,
            "body": f"{message}",
            "typing_time": 0,
            "view_once": True,
        }
    )
    headers = {
        "Authorization": f"Bearer {settings.TOKEN_WHATSAPP}",
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.URL_MESSANGER, data=data, headers=headers) as response:
            return response


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> ShowUser:
    decoded = JWT.decode_jwt(token=token)
    user_id = decoded.get("sub")
    user = await _get_user_by_user_id_for_auth(user_id=user_id, session=db)
    if user is not None:
        return user
