from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class UserBase(BaseModel):
    unique_id: str


class UserCreate(UserBase):
    email_address: str
    password: str


class User(UserBase):
    id: int
    email_address: str
    first_name: str
    last_name: str
    phone_number: str
    is_active: bool
    notification_for_accounts: list[str] = []

    class Config:
        # orm_mode = True
        from_attributes = True
