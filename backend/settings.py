import os
from pathlib import Path
from typing import List

from envparse import Env

env = Env()

BASE_DIR = Path(__file__).parent.parent

ALLOW_ORIGINS: List = env.list(
    "ALLOW_ORIGINS",
    default=[
        "http://localhost",
        "http://localhost:8000",
    ],
)

DATABASE_URL = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
            f"{os.environ.get('DATABASE')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}",
)

ALGORITHM: str = env.str("ALGORITHM", default="RS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
