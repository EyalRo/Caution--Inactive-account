from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post("/users/", tags=["admin"])
async def create_new_user(token: Annotated[str, Depends(oauth2_sceme)]):
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        is_admin = payload.get("isAdmin")
        if not is_admin:
            raise HTTPException(status_code=403, detail="Only admins are allowed to perform this action")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        new_user = await crud.create_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")

    return new_user


    @router.delete("/users/", tags=["admin"])
    async def delete_user(token: Annotated[str, Depends(oauth2_sceme)]):
        """
        Delete a user by ID.

        Args:
            
    user_id: The ID of the user to delete.

        Returns:
            None

        Raises:
            HTTPException: If the user does not exist or there is a server error.
        """
        try:
            # Check if the user exists
            existing_user = await crud.get_user_by_id(id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")

            # Delete the user document
            await db.delete(existing_user["_id"], existing_user["_rev"])

        except Exception as e:
            raise HTTPException(status_code=500, detail="Server Error")

    @router.get("/users", tags=["admin"])
    async def get_all_users():
        """
        Get a list of all users.

        Returns:
            A list of User objects.
        """
        try:
            # Query all user documents
            users = await db.all_docs(include_docs=True)

            # Convert documents to User objects
            user_list = [User(**user["doc"]) for user in users["rows"]]

            return user_list

        except Exception as e:
            raise HTTPException(status_code=500, detail="Server Error")
