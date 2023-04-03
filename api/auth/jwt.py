from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.exceptions import HTTPException
import os
import sys
from jose import JWTError
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    return encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(user_id: Union[str, Any]) -> str:
    refresh_token_data = {
        'user_id': str(user_id),
        'type': 'refresh',
        'exp': datetime.now(timezone.utc)
        + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.now(timezone.utc),
    }
    try:
        refresh_token = encode(refresh_token_data, settings.SECRET_KEY, algorithm="HS256")
    except JWTError:
        refresh_token = None
    return refresh_token

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def decode_access_token(token: str):
    try:
        return decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except PyJWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return username
