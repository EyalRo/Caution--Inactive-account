from fastapi import APIRouter, Depends, HTTPException
from ..database import SessionLocal

from ..dependencies import get_query_token, get_token_header


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_contacts():
    return [{"username": "Rick"}, {"username": "Morty"}]
