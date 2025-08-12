from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime 

class UserBase (BaseModel):
    id:int
    username: str
    

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    fullname: str
    password: str
    preferences: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None 
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserHistoryResponse(BaseModel):
    # user_id:  
    base_currency: str
    target_currency: str
    rate: float
    date: datetime

    model_config = ConfigDict(from_attributes=True)

class UserPreferences(BaseModel):
    base_currency:str
    target_currency: str

    model_config = ConfigDict(from_attributes=True)

class UserPreferencesResponse(BaseModel):
    message: str
    favorites: list[UserPreferences]

    model_config = ConfigDict(from_attributes=True)






