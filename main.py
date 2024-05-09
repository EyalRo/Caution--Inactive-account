from datetime import datetime, timedelta, timezone
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from jose import JWTError, jwt

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import users, contacts

from .data import crud, schemas

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")


app = FastAPI(
    title="Caution! ⚠️ Inactive Accounts.",
    description="API backend for ther service. Implemented in Python using FastAPI, Pydantic, jose, and other good stuff ❤️",
    summary="Backend for Inactive Accounts service.",
    version="0.0.1 pre-alpha",
)  # (dependencies=[Depends(get_query_token)])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login/", tags=["auth"])
def login(user: schemas.UserLogin):
    try:
        userdata = crud.get_user_by_email_and_password(
            user.email_address, user.password
        )
    except:
        err = HTTPException(status_code=404, detail="Not Found")
        return err
    finally:
        access_token = create_access_token(data={"sub": userdata})
        return JSONResponse(content=access_token)


app.include_router(users.router)
app.include_router(contacts.router)
app.include_router(admin.router)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    if SECRET_KEY != None:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    else:
        raise HTTPException(status_code=500, detail="!!! No Secret Key !!!")
    return encoded_jwt
