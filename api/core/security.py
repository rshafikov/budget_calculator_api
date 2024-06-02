from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from api.core import settings

from api.schemas.user_schemas import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(user_tg_id: str, user_role: Role = Role.USER):
    return jwt.encode(
        {
            "sub": user_tg_id,
            "exp": datetime.now()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "role": user_role.value,
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
