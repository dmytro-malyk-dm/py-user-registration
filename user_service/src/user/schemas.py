from datetime import date

from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    date_of_birthday: date
    password: str


class UserLoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    message: str


class CurrentUserDTO(BaseModel):
    id: int
    email: str
