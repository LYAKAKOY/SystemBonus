import os
from typing import List

from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
    f"{os.environ.get('DATABASE')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}",
)

ALGORITHM: str = env.str("ALGORITHM", default="RS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

ALLOW_ORIGINS: List = env.list(
    "ALLOW_ORIGINS",
    default=[
        "http://localhost",
        "http://localhost:8000",
    ],
)