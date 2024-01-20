from starlette import status

from api.actions.auth import get_current_user_from_token
from api.actions.users import _create_user
from api.handlers.users.schemas import CreateUser, ShowUser, CreatedUser
from db.session import AsyncSession
from db.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends

from db.users.models import User

user_router = APIRouter()


@user_router.get("", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get_current_user(
        current_user: User = Depends(get_current_user_from_token)
) -> ShowUser:
    return ShowUser(phone=current_user.phone, is_verified_phone=current_user.is_verified_phone)


@user_router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=CreatedUser)
async def registration_user(
        body: CreateUser,
        db: AsyncSession = Depends(get_db)
) -> CreatedUser:
    user = await _create_user(phone=body.phone, password=body.password, session=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user with such a phone already exists")
    return user
