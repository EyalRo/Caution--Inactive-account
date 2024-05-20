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
        user_id = payload.get("id")
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
