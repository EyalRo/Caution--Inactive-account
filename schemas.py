from pydantic import BaseModel
from datetime import date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    phone_number: str


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True


class NetworkAccountBase(BaseModel):
    account_name: str
    last_update: date
    network: int
    managed_by_user: int


class NetworkAccountCreate(NetworkAccountBase):
    pass


class NetworkAccount(NetworkAccountBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    contacts: list[Contact] = []
    accounts: list[NetworkAccount] = []

    class Config:
        orm_mode = True
