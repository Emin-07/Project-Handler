from src.api.v1.auth import utils as auth_utils
from jwt import InvalidTokenError
from fastapi.security import (
    # HTTPBearer,
    # HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
    HTTPBasicCredentials,
    HTTPBasic,
)
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response, Form
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.queries import employee, get_session
import secrets
from datetime import datetime


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/jwt", tags=["JWT"])
security = HTTPBasic()
# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


async def validate_auth_user(
    username: str = Form(), password: str = Form(), session=Depends(get_session)
):
    users = await employee.get_all_users(session)
    for user in users:
        if user.first_name == username:
            user_pwd_hex: str = await employee.get_user_pwd(
                employee_id=user.id, session=session
            )
            if auth_utils.validate_password(password, user_pwd_hex):
                return UserSchema(username=username, password=password)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or username"
    )


async def auth_logged_in_user(
    creds: HTTPBasicCredentials = Depends(security), session=Depends(get_session)
):
    return await validate_auth_user(creds.username, creds.password, session)


COOKIE: dict[str, dict] = {}
COOKIE_SESSION_ID_KEY = "web-session-id"


def generate_session_id():
    return secrets.token_hex()


@router.post("/login-cookie/")
async def auth_login_user(response: Response, username=Depends(auth_logged_in_user)):
    session_id = generate_session_id()
    COOKIE[session_id] = {"username": username, "logged_in_at": datetime.now()}
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"status": "ok"}


def get_session_data(session_id=Cookie(alias=COOKIE_SESSION_ID_KEY)) -> dict:
    if session_id not in COOKIE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    return COOKIE[session_id]


@router.get("/check-cookie/")
async def auth_check_user(user_session_data: dict = Depends(get_session_data)):
    user = user_session_data["username"]
    return {"message": f"Hi, {user.username}", **user_session_data}


@router.delete("/delete-cookie/")
async def auth_delete_cookie(
    response: Response,
    session_id=Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIE.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return {"message": f"Farewell {user_session_data['username'].username}"}


# JWT


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Token : {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload), session=Depends(get_session)
):
    username: str | None = payload.get("sub")
    users = await employee.get_all_users(session)
    for user in users:
        if user.first_name == username:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {"sub": user.username, "password": user.password}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/check/")
def auth_person_check(
    payload: dict = Depends(get_current_token_payload),
    user=Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "salary": user.salary,
        "is_working": user.is_working,
        "logged_in_at": iat,
    }
