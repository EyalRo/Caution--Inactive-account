import couchdb, os, hashlib
from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("DB_STRING")
SECRET_KEY = os.getenv("SECRET_KEY")


if DB_STRING:
    couch = couchdb.Server(DB_STRING)
    db = couch["inactive-account"]


def get_user_by_email_and_password(email: str, password: str):
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    mango = {
        "selector": {
            "email_address": email,
            "password_hash": hashed_password,
        },
        "limit": 1,
    }

    for user in db.find(mango):
        return user
    return None
