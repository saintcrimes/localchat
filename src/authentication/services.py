from sqlalchemy.ext.asyncio import AsyncSession
from models import users as Users
from sqlalchemy import select, or_
from fastapi import HTTPException, status

async def get_user_by_login_identifier(db_session: AsyncSession, login_identifier: str) -> Users:
    query = select(Users).where(or_(Users.username == login_identifier, Users.email == login_identifier))
    result = await db_session.execute(query)
    user: Users | None = result.scalar_one_or_none()
    return user

async def get_data_by_email(db_session: AsyncSession, email: str):
    query = select(Users).where(Users.email == email)
    result = await db_session.execute(query)
    user: Users | None = result.scalar_one_or_none()
    return user

async def get_user_guid_by_username(*, username: str, db_session):

    query = select(Users).where(Users.username == username)
    result = await db_session.execute(query)

    user: Users | None = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found :(")

    user_guid = user.guid

    return user_guid
