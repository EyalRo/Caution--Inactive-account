from pydantic import BaseModel

class UserBase(BaseModel):
    id: str
    email_address: str
    password: str


class UserLogin(UserBase):
    pass


class User(UserBase):
    first_name: str
    last_name: str
    phone_number: str