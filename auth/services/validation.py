from fastapi import Depends, Form, HTTPException, status
from jwt import InvalidTokenError

from auth.utils import utils as auth_utils
from auth.utils.helper import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    oauth2_scheme,
    temp_db,
)

# async def validate_auth_user(
#     username: str = Form(), password: str = Form(), session=Depends(get_session)
# ):
#     users = await employee.get_all_users(session)
#     for user in users:
#         if user.first_name == username:
#             user_pwd_hex: str = await employee.get_user_pwd(
#                 employee_id=user.id, session=session
#             )
#             if auth_utils.validate_password(password, user_pwd_hex):
#                 return UserSchema(sub=username, password=password)
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or username"
#     )


async def validate_auth_user(username: str = Form(), password: str = Form()):
    if user := temp_db.get(username):
        if auth_utils.validate_password(
            password, (auth_utils.hash_password(user.password).hex())
        ):
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or username"
    )


def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Token : {e}",
        )
    return payload


# async def get_user_by_sub(payload: dict, session=Depends(get_session)):
#     username: str | None = payload.get("sub")
#     users = await employee.get_all_users(session)
#     for user in users:
#         if user.first_name == username:
#             return user
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="token invalid (user not found)",
#     )


def get_user_by_sub(payload: dict) -> dict:
    username: str | None = payload.get("sub")
    if user := temp_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def validate_token_type(payload: dict, expected_token_type: str):
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type == expected_token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Expected token {expected_token_type!r} type doesn't match the actual token type {token_type!r}",
    )


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: dict = Depends(get_current_token_payload)):
        validate_token_type(payload, self.token_type)
        return get_user_by_sub(payload)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)
