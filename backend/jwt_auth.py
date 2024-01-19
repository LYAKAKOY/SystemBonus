from datetime import timedelta, datetime
import jwt

import settings


class JWT:
    @staticmethod
    def encode_jwt(
            payload: dict,
            private_key: str = settings.private_key_path.read_text(),
            algorithm: str = settings.ALGORITHM,
            expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @staticmethod
    def decode_jwt(
            token: str | bytes,
            public_key: str = settings.public_key_path.read_text(),
            algorithm: str = settings.ALGORITHM,
    ) -> dict:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
