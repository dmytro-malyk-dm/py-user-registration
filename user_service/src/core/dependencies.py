from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from user_service.src.user.schemas import CurrentUserDTO
from user_service.src.security.token_manager import decode_access_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUserDTO:
    """
    Get current user from JWT token WITHOUT database query.

    Parses JWT payload into CurrentUserDTO Pydantic schema.
    This is the main authentication dependency - fast and efficient.

    For cases requiring full SQLAlchemy User object (password operations,
    relationships), use get_full_user() dependency instead.

    Returns:
        CurrentUserDTO: Pydantic model with user data from token

    Raises:
        HTTPException 401: Invalid or expired token
        HTTPException 403: Inactive user
    """

    token = credentials.credentials

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        current_user = CurrentUserDTO(
            id=int(payload["sub"]),
            email=payload["email"],
        )
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user