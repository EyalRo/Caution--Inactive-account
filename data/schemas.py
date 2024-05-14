from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    token: str


# Schemas for Users


# Common for all user interactions
class UserBase(BaseModel):
    email_address: str
    password: str


# Nothing extra needed for Login
class UserLoginData(UserBase):
    pass


# All single user data
class User(UserLoginData):
    unique_id: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
