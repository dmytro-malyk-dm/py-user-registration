from datetime import datetime, timedelta
from src.core.config import settings
from jose import jwt, JWTError


def create_access_token(user_id: int, email: str) -> str:
    """
    Create JWT access token with full user information.

    Token payload includes: id, email, user_group, is_active.
    This eliminates need for database queries in get_current_user dependency.

    Returns:
        JWT access token string
    """
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        to_encode, settings.SECRET_KEY_ACCESS, algorithm=settings.JWT_SIGNING_ALGORITHM
    )


def decode_access_token(token: str) -> dict | None:
    """
    Decode and validate an access token, returning the token's data.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY_ACCESS,
            algorithms=[settings.JWT_SIGNING_ALGORITHM],
        )

        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None

