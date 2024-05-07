import couchdb
from . import models, schemas


def get_user_by_email(email: str):
    return ()


def get_user_by_email_and_password(email: str, password: str):
    hashed_password = password
    return ()


def get_users(skip: int = 0, limit: int = 100):
    return ()


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email_address, hashed_password=fake_hashed_password
    )
    return()