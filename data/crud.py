import couchdb, os, hashlib
from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("DB_STRING")


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


def get_user_by_id(id: str):
    mango = {"selector": {"_id": id}}

    for user in db.find(mango):
        return user
    return None

async def create_user(user: User):
    """
    Create a new user.

    Args:
        user: The user data to create.

    Returns:
        The created user.

    Raises:
        HTTPException: If the user already exists or there is a server error.
    """
    try:
        # Check if the user already exists
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")

        # Create the new user
        new_user = await db.insert_one(user.dict())

        return new_user

    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")
async def update_user(user_id: str, user: User):
    """
    Update an existing user.

    Args:
        user_id: The ID of the user to update.
        user: The updated user data.

    Returns:
        The updated user.

    Raises:
        HTTPException: If the user does not exist or there is a server error.
    """
    try:
        # Check if the user exists
        existing_user = await get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the user document
        await db.update_one({"_id": user_id}, {"$set": user.dict()})

        # Fetch the updated user
        updated_user = await get_user_by_id(user_id)

        return updated_user

    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")
