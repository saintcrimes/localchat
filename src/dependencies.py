from typing import Annotated
import jwt
from fastapi import Cookie, Depends, HTTPException, status
from models import users as Users
from sqlalchemy.ext.asyncio import AsyncSession
from Config import settings
from base import get_db
from authentication.services import (
    get_user_by_login_identifier
)



async def get_current_user(
    access_token: Annotated[str | None, Cookie()],
    db_session: AsyncSession = Depends(get_db),
) -> Users:
    try:
        payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHMS])
        login_identifier: str = payload.get("sub") #email or username
        if not login_identifier:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Users | None = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

