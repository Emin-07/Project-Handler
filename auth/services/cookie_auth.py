import secrets
from datetime import datetime

from fastapi import Cookie, Depends, HTTPException, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from ..routes.jwt_auth import validate_auth_user

COOKIE: dict[str, dict] = {}
COOKIE_SESSION_ID_KEY = "web-session-id"
security = HTTPBasic()


async def auth_logged_in_user(creds: HTTPBasicCredentials = Depends(security)):
    return await validate_auth_user(creds.username, creds.password)


def generate_session_id():
    return secrets.token_hex()


# @router.post("/login-cookie/")
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


# @router.get("/check-cookie/")
async def auth_check_user(user_session_data: dict = Depends(get_session_data)):
    user = user_session_data["username"]
    return {"message": f"Hi, {user.username}", **user_session_data}


# @router.delete("/delete-cookie/")
async def auth_delete_cookie(
    response: Response,
    session_id=Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIE.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return {"message": f"Farewell {user_session_data['username'].username}"}
