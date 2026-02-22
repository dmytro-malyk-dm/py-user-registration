
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.user import create_user, get_user_by_email
from src.database.database import get_async_session
from src.schemas.user import UserRegisterSchema, UserResponseSchema, UserLoginSchema, UserLoginResponseSchema
from src.security.password import verify_password
from src.security.token_manager import create_access_token

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/register/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user. User must activate account via activation token.",
)
async def register(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Register new user
    Creates a new user account with the provided email and password.
    User account is created in inactive state and requires email activation.
    """

    existing_user = await get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist"
        )
    await create_user(session, user_data)
    return UserResponseSchema(message="User registered successfully")



@router.post(
    "/login/",
    response_model=UserLoginResponseSchema,
    summary="Login",
    description="Login and receive access token. Refresh token is issued together.",
)
async def login(
    credentials: UserLoginSchema, session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticate user and generate JWT tokens.

    Validates user credentials and returns access and refresh tokens.
    User must have an activated account to login.
    """
    user = await get_user_by_email(session, credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = create_access_token(
        user_id=user.id,
        email=user.email
    )
    return UserLoginResponseSchema(access_token=token)
