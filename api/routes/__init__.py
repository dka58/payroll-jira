from fastapi import APIRouter

from .auth import auth_router
from .users import users_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(users_router, prefix='/user', tags=['users'])
