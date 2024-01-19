import uuid
from typing import Annotated
from annotated_types import MinLen, MaxLen
from fastapi import HTTPException
from pydantic import field_validator

from api.base_schemas import TunedModel


class CreateUser(TunedModel):
    phone: Annotated[str, MinLen(11), MaxLen(11)]
    password: Annotated[str, MinLen(4)]

    @field_validator("phone")
    def validate_phone(cls, value: str):
        if not value.isdigit():
            raise HTTPException(
                status_code=422, detail="phone must contains only numbers"
            )
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "phone": "79280807437",
                    "password": "pass",
                }
            ]
        }
    }


class CreatedUser(TunedModel):
    user_id: uuid.UUID


class Token(TunedModel):
    access_token: str
    token_type: str
