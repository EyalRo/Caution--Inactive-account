from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(Authorization: Annotated[str, Header()]):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Auth Token Missing")
