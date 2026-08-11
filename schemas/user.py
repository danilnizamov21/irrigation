from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    login: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=8, max_length=50)


class UserRegister(BaseModel):
    login: str = Field(min_length=1, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UserResponse(BaseModel):
    login: str
    email: str
    role: str
