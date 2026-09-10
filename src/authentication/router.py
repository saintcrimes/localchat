from fastapi import APIRouter, Depends, HTTPException, Response
from .schemas import AuthSchema
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from base import get_db
from .services import get_data_by_email
import logging
import bcrypt
from fastapi.responses import RedirectResponse
import jwt
from utils import create_access_token
import logging

logging.getLogger(__name__)


router = APIRouter()

session = Annotated[AsyncSession, Depends(get_db)]

@router.post("/v1/auth/authentication")
async def authentication(data: AuthSchema, session: session):

    data_from_db = await get_data_by_email(db_session=session, email=data.email)

    if data_from_db is None:
        raise HTTPException(
            409,
            "Username or password is incorrect!")

    hash = data_from_db.password

    logging.info(hash)

    is_password = bcrypt.checkpw(
        data.password.encode("utf-8"),
        hash.encode("utf-8")
    )

    if is_password is False:
        raise HTTPException(409, "Incorrect credentials!")


    access_token: str = create_access_token(data.email)
    
    redirect = RedirectResponse(
        url="/",
        status_code=303
    )
    redirect.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax", secure=True)

    return redirect