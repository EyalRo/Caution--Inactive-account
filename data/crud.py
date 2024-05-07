import couchdb, os
from . import schemas
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("DB_STRING")

if DB_STRING:
    couch = couchdb.Server(DB_STRING)
    db = couch["inactive-account"]

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email_and_password(email: str, password: str):
    hashed_password = get_password_hash(password)
    mango = {"selector": {"email_address": email, "password_hash": hashed_password}}
    db.find(mango)
    return ()


def get_password_hash(password):
    return pwd_context.hash(password)
