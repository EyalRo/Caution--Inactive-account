from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_query_token, get_token_header

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_contacts():
    return [{"username": "Rick"}, {"username": "Morty"}]