from fastapi import APIRouter, Depends, HTTPException

from api.auth.jwt import get_current_user
from api.models import User, UserInDB, UserUpdate, UserCreate
from api.dependencies.users import UserRepository


users_router = APIRouter()


@users_router.get('/me', response_model=UserInDB)
async def read_current_user(current_user: UserInDB = Depends(get_current_user)):
    """
    Retrieve information about the current user.
    """
    return current_user


@users_router.put('/me', response_model=UserUpdate)
async def update_current_user(
    user: UserUpdate, 
    current_user: UserInDB = Depends(get_current_user)
) -> User:
    """
    Update information about the current user.
    """
    db_user = await UserRepository.get_user_by_username(current_user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return await UserRepository.update_user(db_user.id, user)


@users_router.post('/create', response_model=UserCreate)
async def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new user.
    """
    return await UserRepository.create_user(user)


