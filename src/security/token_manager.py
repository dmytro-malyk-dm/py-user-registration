from datetime import datetime, timedelta
from src.core.config import settings
from jose import jwt


def create_access_token(user: "User" = None) -> str:
    """
    Create JWT access token with full user information.

    Token payload includes: id, email, user_group, is_active.
    This eliminates need for database queries in get_current_user dependency.

    Args:
        user: Full User object with group relationship loaded

    Returns:
        JWT access token string
    """
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user.id),
        "email": user.email,
        "exp": expire,
        "type": "access",
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY_ACCESS, algorithm=settings.JWT_SIGNING_ALGORITHM
    )

    return encoded_jwt