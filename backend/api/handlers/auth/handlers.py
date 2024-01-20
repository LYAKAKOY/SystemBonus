from typing import Annotated

from annotated_types import MinLen, MaxLen
from starlette import status
from api.actions.auth import authenticate_user, send_message_to_whatsapp, generate_code, _get_user_by_phone_for_auth
from api.actions.users import _update_user
from api.handlers.auth.schemas import Token
from api.handlers.users.schemas import UpdatedUser
from db.cache.session import get_redis
from db.session import AsyncSession
from db.session import get_db
from fastapi import APIRouter, Form, HTTPException
from fastapi import Depends
from jwt_auth import JWT
from redis import asyncio as aioredis

auth_router = APIRouter()


@auth_router.post("/send_confirmation_code", status_code=status.HTTP_200_OK)
async def send_confirmation_code_to_phone(
        phone: Annotated[str, MinLen(11), MaxLen(11)],
        db: AsyncSession = Depends(get_db),
        redis: aioredis.client = Depends(get_redis)):
    user = await _get_user_by_phone_for_auth(phone=phone, session=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is not registered")
    code = generate_code()
    await redis.set(phone, code, 900)
    response = await send_message_to_whatsapp(phone=phone, message=f"Your confirmation code: {code}")
    if response.status != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"detail": "code has been sent"}


@auth_router.post("/verify_phone", status_code=status.HTTP_200_OK, response_model=UpdatedUser)
async def verify_phone(
        phone: Annotated[str, MinLen(11), MaxLen(11)],
        code: Annotated[str, MinLen(4), MaxLen(4)],
        db: AsyncSession = Depends(get_db),
        redis: aioredis.client = Depends(get_redis)) -> UpdatedUser:
    user = await _get_user_by_phone_for_auth(phone=phone, session=db)
    code_from_db = await redis.get(phone)
    if code == code_from_db.decode('utf-8'):
        user_id = await _update_user(user_id=user.user_id, is_active=True, is_verified_phone=True, session=db)
        if user_id is not None:
            return user_id
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect code")


@auth_router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(
        phone: Annotated[str, Form(min_length=11, max_length=11)],
        password: Annotated[str, Form(min_length=4)],
        db: AsyncSession = Depends(get_db)
) -> Token:
    user = await authenticate_user(phone, password, db)
    access_token = JWT.encode_jwt(
        payload={"sub": str(user.user_id)}
    )
    return Token(access_token=access_token, token_type="bearer")