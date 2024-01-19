import uuid

from api.base_schemas import TunedModel


class CreatedUser(TunedModel):
    user_id: uuid.UUID
