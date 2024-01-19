from pydantic import BaseModel


class TunedModel(BaseModel):
    class ConfigDict:
        from_attributes = True


class Token(TunedModel):
    access_token: str
    token_type: str
