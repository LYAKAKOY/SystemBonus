import os
from pathlib import Path
from typing import List

from envparse import Env

env = Env()

BASE_DIR = Path(__file__).parent

ALLOW_ORIGINS: List = env.list(
    "ALLOW_ORIGINS",
    default=[
        "http://localhost",
        "http://localhost:8000",
    ],
)

REDIS_URL: str = env.str(
    "REDIS_URL",
    default=f"redis://{os.environ.get('REDIS_USER')}:{os.environ.get('REDIS_PASSWORD')}@"
            f"{os.environ.get('REDIS_DB')}:{os.environ.get('REDIS_PORT')}"
)

DATABASE_URL: str = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
            f"{os.environ.get('DATABASE')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}",
)

ALGORITHM: str = env.str("ALGORITHM", default="RS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"

TOKEN_WHATSAPP: str = env.str(
    "TOKEN_WHATSAPP",
    default="f33t83rHQcnxgyjgm921e4y7J0smqZUq"
)

URL_MESSANGER: str = env.str(
    "URL_MESSANGER",
    default="https://gate.whapi.cloud/messages/text"
)
