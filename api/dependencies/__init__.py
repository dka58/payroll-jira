from fastapi import Depends

from api.auth.jwt import get_current_user


def get_current_active_user(current_user: str = Depends(get_current_user)):
    """
    Dependency to get the current active user based on the JWT token.
    """
    # Your logic to check if the user is active
    return current_user
