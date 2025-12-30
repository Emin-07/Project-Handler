from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel

from .utils import auth_config, encode_jwt


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserSchema(BaseModel):
    sub: str
    password: str


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")
router = APIRouter(prefix="/jwt", tags=["Auth"], dependencies=[Depends(http_bearer)])


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


admin = UserSchema(sub="admin", password="admin")
john = UserSchema(sub="john", password="qwerty")
temp_db: dict = {john.sub: john, admin.sub: admin}


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = auth_config.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_time_delta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {"sub": user.sub, "password": user.password}
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=auth_config.access_token_expire_minutes,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {"sub": user.sub}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=auth_config.refresh_token_expire_days),
    )
