import os
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt


from ..data import crud, schemas

from ..dependencies import get_query_token, get_token_header

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
ISSUER = os.getenv("ISSUER")

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


@router.get("/")
def validateToken():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJTdGFyZHVzdC1BUEkiLCJuYmYiOjE3MTU3MDMyOTQsImlhdCI6MTcxNTcwMzI5NCwiZXhwIjoxNzE1NzA0MTk0LCJkYXRhIjp7Il9pZCI6IjI4ZWIyM2RiYzE5YWMwOTIxOTEyNTc3NTVhMDBkNjQ4IiwiX3JldiI6IjQtOGVlNjA2YjhhZmZjYTkxNGY2MDQ4NTFjOGIxMDM2MWEiLCJlbWFpbF9hZGRyZXNzIjoidGVzdEB0ZXN0LmNvbSIsInBhc3N3b3JkX2hhc2giOiJmNjYwYWI5MTJlYzEyMWQxYjFlOTI4YTBiYjRiYzYxYjE1ZjVhZDQ0ZDVlZmRjNGUxYzkyYTI1ZTk5YjhlNDRhIn19.v3Vpo7hkpxN50w8dfCLS9m2FCFmyLev_PFg8zSs5ZX4"
    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="No Secret Key")
    decoded = jwt.decode(token, SECRET_KEY, issuer=ISSUER)
    return decoded["data"]
