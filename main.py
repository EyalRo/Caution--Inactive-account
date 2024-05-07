from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import users, contacts

from .data import crud, schemas

app = FastAPI()  # (dependencies=[Depends(get_query_token)])


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
        token = crud.get_user_by_email_and_password(user.email_address, user.password)
    except:
        err = HTTPException(status_code=404, detail="Not Found")
        return(err)
    finally:
        return JSONResponse(content=token)


app.include_router(users.router)
app.include_router(contacts.router)
app.include_router(admin.router)
