from fastapi import Depends

from ..services.validation import (
    get_current_auth_user,
    get_current_auth_user_for_refresh,
    get_current_token_payload,
    validate_auth_user,
)
from ..utils.helper import (
    TokenInfo,
    UserSchema,
    create_access_token,
    create_refresh_token,
    router,
)


@router.post("/login/", response_model=TokenInfo, response_model_exclude_none=True)
def auth_user_issue_jwt_access(user: UserSchema = Depends(validate_auth_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
def auth_user_issue_jwt_refresh(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/check/")
def auth_person_check(
    payload: dict = Depends(get_current_token_payload),
    user=Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        **user.model_dump(),
        "logged_in_at": iat,
    }
