from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class Users(BaseModel):
    id: int
    username: str
    email: str
    owner: str


class Login(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False

    class Config:
        orm_mode = True


class Register(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str
    owner: str

    class Config:
        orm_mode = True

    @validator('username')
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v

    @validator("password1")
    def checkPass(cls, v, values, **kwargs):
        if 'password2' in values and v != values['password2']:
            raise ValueError('passwords do not match')
        return v
