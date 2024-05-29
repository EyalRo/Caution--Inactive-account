from datetime import datetime, timedelta
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from .internal import admin
from .routers import users, contacts

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
ISSUER = os.getenv("ISSUER")


app = FastAPI(
    title="Caution! Inactive Accounts",
    description="API backend for ther service. Implemented in Python using FastAPI, Pydantic, jose, and other good stuff ❤️",
    summary="Backend for Inactive Accounts service.",
    version="0.0.1 pre-alpha",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


"""



@app.post("/login/", tags=["auth"])
def get_token(user: schemas.UserLoginData):
    try:
        userdata = crud.get_user_by_email_and_password(
            user.email_address, user.password
        )
    except:
        err = HTTPException(status_code=500, detail="Server Error")
        return err
    finally:
        if userdata is None:
            raise HTTPException(status_code=401, detail="No such user")
        token_data = {
            "id": userdata["_id"],
            "isAdmin": userdata["admin"],
            "email_address": userdata["email_address"],
        }
        print(token_data)
        access_token = create_access_token(
            data={
                "iss": ISSUER,  # Issuer Claim
                "nbf": datetime.now(),  # Not Before Claim
                "iat": datetime.now(),  # Issued At Claim
                "exp": datetime.now() + timedelta(minutes=60),  # Expiration Time
                "data": token_data,
            }
        )
        return JSONResponse(content=access_token)


@app.post("/signup/", tags=["auth"])
def sign_up(user: schemas.UserLoginData):
    try:
        userdata = crud.create_user(user.email_address, user.password)
    except:
        err = HTTPException(status_code=500, detail="Server Error")
        return err
    finally:
        if userdata is None:
            raise HTTPException(status_code=500, detail="Server Error")
        return JSONResponse(content=user)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/validate/", tags=["auth"])
def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):

    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="!!! No Secret Key !!!")
    try:
        decoded = jwt.decode(token, SECRET_KEY, issuer=ISSUER)
    except:
        return "JWT Error"
    finally:
        return decoded["data"]


app.include_router(users.router)
app.include_router(contacts.router)
app.include_router(admin.router)


def create_access_token(data: dict):
    to_encode = data.copy()
    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="!!! No Secret Key !!!")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    
"""
