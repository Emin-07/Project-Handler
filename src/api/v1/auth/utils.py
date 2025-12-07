import jwt
import bcrypt
from src.api.v1.schemas import AuthJWT
from datetime import datetime, timedelta

auth_config = AuthJWT()


def encode_jwt(
    payload: dict,
    key: str = auth_config.private_key_path.read_text(),
    algorithm: str = auth_config.algorithm,
    expire_minutes: int = auth_config.access_token_expire_minutes,
    expire_time_delta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_time_delta:
        expires_at = now + expire_time_delta
    else:
        expires_at = now + timedelta(minutes=expire_minutes)

    to_encode.update(iat=now)
    to_encode.update(exp=expires_at)

    encoded = jwt.encode(to_encode, key, algorithm)
    return encoded


def decode_jwt(
    jwt_token: str | bytes,
    key: str = auth_config.public_key_path.read_text(),
    algorithm: str = auth_config.algorithm,
):
    decoded = jwt.decode(jwt_token, key, algorithm)
    return decoded


def hash_password(pwd) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = pwd.encode()

    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hexed_and_hashed_pwd: str) -> bool:
    hashed_pwd: bytes = bytes.fromhex(hexed_and_hashed_pwd)

    return bcrypt.checkpw(password.encode(), hashed_pwd)
