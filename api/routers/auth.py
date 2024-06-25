import logging
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.core import settings
from api.core.security import create_token, verify_password
from api.schemas.auth import Token
from api.schemas.user_schemas import Role, User
from api.services.user_service import UserService, get_user_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])

token_security = OAuth2PasswordBearer(tokenUrl="/auth/token")

logger = logging.getLogger(__name__)


def check_token(enc_token: Annotated[str, Depends(token_security)]) -> dict:
    try:
        return jwt.decode(
            enc_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

    except jwt.ExpiredSignatureError as err:
        logger.error('Expired token %r: %s', enc_token, err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    except jwt.InvalidTokenError as err:
        logger.error('Invalid token %r: %s', enc_token, err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token can't be decoded",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def authenticate_user(
    telegram_id: str, password: str, user_service: UserService
) -> User | None:
    user = await user_service.get_user(telegram_id=telegram_id)

    if not user or not verify_password(password, user.password):
        return None

    return user


def rbac(roles: set[Role]):
    def validate_role(token_payload: dict = Depends(check_token)) -> dict:
        roles.add(Role.ADMIN)

        if Role(token_payload["role"]) not in roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed"
            )

        return token_payload

    return validate_role


async def get_auth_user(
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_payload: Annotated[dict, Depends(rbac({Role.USER}))],
) -> User:
    return await user_service.get_user_or_404(telegram_id=user_payload["sub"])


@auth_router.post("/token", status_code=status.HTTP_201_CREATED)
async def token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Token:
    user = await authenticate_user(form.username, form.password, user_service)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Check your credentials"
        )

    return Token(
        access_token=create_token(user.telegram_id, user.role),
        token_type="bearer"
    )
