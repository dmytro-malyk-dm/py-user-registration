from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.src.user.models import UserModel
from user_service.src.user.schemas import UserRegisterSchema
from user_service.src.security.password import hash_password


async def create_user(session: AsyncSession, user_data: UserRegisterSchema) -> UserModel:

     new_user = UserModel(
         email=str(user_data.email)
     )
     new_user.hashed_password = hash_password(user_data.password)
     new_user.name = user_data.name
     new_user.surname = user_data.surname
     new_user.date_of_birthday = user_data.date_of_birthday
     session.add(new_user)
     try:
         await session.flush()
         await session.commit()
         await session.refresh(new_user)
     except IntegrityError:
         await session.rollback()
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
         )
     return new_user


async def get_user_by_email(session: AsyncSession, email: str) -> UserModel | None:
    result = await  session.execute(
        select(UserModel).where(UserModel.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> UserModel | None:
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    return result.scalar_one_or_none()
