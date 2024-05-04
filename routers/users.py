from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional

from ..dependencies import get_query_token, get_token_header

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class User(BaseModel):
    unique_id: str
    first_name: str
    last_name: str
    email_address: str
    password: str
    phone_number: Optional[str] = None
    notify_list: list = []


engine = create_engine("sqlite:///database.db")


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
