from pydantic import BaseModel


class Token(BaseModel):
    token: str


# Schemas for Users


# Common for all user interactions
class UserBase(BaseModel):
    email_address: str
    password: str


# Nothing extra needed for Login
class UserLogin(UserBase):
    pass


# All single user data
class User(UserBase):
    first_name: str
    last_name: str
    phone_number: str
