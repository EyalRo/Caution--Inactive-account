from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine
from typing import Optional

from ..database import SessionLocal

from .. import crud, models, schemas

from ..dependencies import get_query_token, get_token_header


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/users",
    tags=["users"],
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


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
