from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.src.user.crud import create_user, get_user_by_email
from user_service.src.core.database import get_async_session
from user_service.src.user.schemas import (
    UserRegisterSchema,
    UserResponseSchema,
    UserLoginSchema,
    UserLoginResponseSchema,
)
from user_service.src.security.password import verify_password
from user_service.src.security.token_manager import create_access_token

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/register/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_async_session),
):
    existing_user = await get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist",
        )
    await create_user(session, user_data)
    return UserResponseSchema(message="User registered successfully")


@router.post(
    "/login/",
    response_model=UserLoginResponseSchema,
    summary="Login",
)
async def login(
    credentials: UserLoginSchema,
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_email(session, credentials.email)

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token(
        user_id=user.id,
        email=user.email,
        name=user.name,
        surname=user.surname,
        date_of_birthday=str(user.date_of_birthday),
    )
    return UserLoginResponseSchema(access_token=token)
