from pydantic import BaseModel

# Schemas for Users

# Common for all user interactions
class UserBase(BaseModel):
    id: str
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