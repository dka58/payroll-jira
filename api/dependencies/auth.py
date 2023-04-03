from fastapi import HTTPException, Header, status, Depends
from api.auth.jwt import decode_access_token
from api.auth.schemas import TokenData

async def get_token_data(authorization: str = Header(...)) -> TokenData:
    """
    Dependency to decode and verify the JWT token sent in the `Authorization` header.
    """
    try:
        bearer, token = authorization.split()
        if bearer != 'Bearer':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid authorization header'
            )
        payload = decode_access_token(token)
        token_data = TokenData(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        ) from e
    return token_data
