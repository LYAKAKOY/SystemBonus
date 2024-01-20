from typing import Annotated

from annotated_types import MinLen, MaxLen
from starlette import status

from api.actions.auth import get_current_user_from_token, _get_user_by_phone_for_auth
from api.actions.users import _create_user, _create_profile
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


@user_router.post("/profile", status_code=status.HTTP_201_CREATED)
async def create_profile(
        phone: Annotated[str, MinLen(11), MaxLen(11)],
        first_name: Annotated[str, MaxLen(20)],
        last_name: Annotated[str, MaxLen(40)],
        db: AsyncSession = Depends(get_db)
):
    user = await _get_user_by_phone_for_auth(phone=phone, session=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with such a phone has not been found")
    profile = await _create_profile(user_id=user.user_id, phone=phone, first_name=first_name, last_name=last_name, session=db)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="This user's profile already exists")
    return profile
