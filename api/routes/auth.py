from fastapi import APIRouter, Depends
from fastapi import HTTPException
from jose import JWTError
from api.auth import create_access_token, create_refresh_token, get_password_hash, verify_password, decode_access_token
from api.auth.schemas import Login, RefreshToken, Token
from api.models import User
from api.dependencies.users import UserRepository

auth_router = APIRouter()


# @auth_router.post('/register', response_model=Token)
# async def register(user: User, user_repo: UserRepository = Depends()) -> Token:
#     """
#     Register a new user and return an access token.
#     """
#     db_user = await user_repo.create_user(user)
#     access_token = create_access_token(data={"sub": db_user.username})
#     return Token(access_token=access_token, token_type="bearer")


@auth_router.post('/token', response_model=Token)
async def login(login: Login) -> Token:
    """
    Authenticate a user and return an access token.
    """
    db_user = await UserRepository.get_user_by_username(login.username)
    if not db_user or not verify_password(login.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@auth_router.post('/refresh', response_model=Token)
async def refresh(refresh_token: RefreshToken) -> Token:
    """
    Generate a new access token using a refresh token.
    """
    try:
        payload = decode_access_token(refresh_token.refresh_token, verify=False)
        username = payload.get('sub')
        if not username:
            raise HTTPException(status_code=400, detail='Invalid refresh token')
        db_user = await UserRepository.user_repo.get_user_by_username(username)
        if not db_user:
            raise HTTPException(status_code=400, detail='Invalid refresh token')
    except JWTError as e:
        raise HTTPException(status_code=400, detail='Invalid refresh token') from e
    access_token = create_access_token(data={"sub": db_user.username})
    return Token(access_token=access_token, token_type="bearer")
