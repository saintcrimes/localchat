from sqlalchemy.ext.asyncio import AsyncSession
from models import users as Users
from sqlalchemy import select, or_

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