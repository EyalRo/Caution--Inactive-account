import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
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
def get_user_data(token: Annotated[str, Depends(oauth2_scheme)]):

    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="!!! No Secret Key !!!")
    try:
        user_id = jwt.decode(token, SECRET_KEY, issuer=ISSUER)["id"]
    except:
        return "JWT Error"
    finally:
        userdata = crud.get_user_by_id(user_id)
        return userdata
