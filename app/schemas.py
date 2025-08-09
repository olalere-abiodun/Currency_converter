from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserBase (BaseModel):
    username: str
    email: EmailStr
    fullname: str

class UserRegister(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)



