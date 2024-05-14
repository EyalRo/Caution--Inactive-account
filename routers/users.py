import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated, Optional
from jose import JWTError, jwt

from ..data import crud, schemas

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
ISSUER = os.getenv("ISSUER")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
def validateToken(token: Annotated[str, Depends(oauth2_scheme)]):

    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="!!! No Secret Key !!!")
    try:
        decoded = jwt.decode(token, SECRET_KEY, issuer=ISSUER)
    except:
        return "JWT Error"
    finally:
        return decoded["data"]
