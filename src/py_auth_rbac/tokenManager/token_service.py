from typing import Dict, Any
import datetime
import jwt


class TokenManager:
    SECRET_KEY = "MI_CLAVE"
    ALGORITHM = "HS256"

    @classmethod
    def crear_token(cls, user_data: Dict[str, Any], expire_minutes: int = 30) -> str:
        payload = user_data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes)

        payload["exp"] = expire

        token = jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def decode_token(cls, token: str) -> str:
        verify_token = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        return verify_token
