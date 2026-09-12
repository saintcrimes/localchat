from sqlalchemy.ext.asyncio import AsyncSession
from models import users as User, Chat, ChatType
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from uuid import UUID
import logging 

logger = logging.getLogger(f"chatapp.{__name__}")

async def direct_chat_exists(db_session: AsyncSession, *, current_user: User, recipient_user: User) -> bool:
    query = select(
        Chat.id
    ).where(
        and_(
            Chat.chat_type == ChatType.DIRECT,
            Chat.is_deleted.is_(False),
            Chat.users.contains(current_user),
            Chat.users.contains(recipient_user),
        )
    )
    result = await db_session.execute(query)
    existing_chat = result.scalar_one_or_none()
    return existing_chat is not None


async def get_user_by_guid(db_session: AsyncSession, guid: UUID) -> User | None:
    query = select(User).where(User.guid == guid)

    result = await db_session.execute(query)
    return result.scalar_one_or_none()
    

async def get_chat_by_guid(db_session: AsyncSession, guid: UUID) -> Chat | None:
    query = select(Chat).where(Chat.guid == guid).options(selectinload(Chat.messages),selectinload(Chat.users), selectinload(Chat.read_statuses))
    result = await db_session.execute(query)
    user: User | None = result.scalar_one_or_none()
    return user



async def create_direct_chat(db_session: AsyncSession, *, initator_user: User, recipient_user: User) -> Chat:

    try:
        chat = Chat(chat_type=ChatType.DIRECT)
        chat.users.append(initator_user)
        chat.users.append(recipient_user)
        db_session.add(chat)
        await db_session.commit()

    except Exception as exc_info:
        await db_session.rollback()
        logger.error(f"LOOK AT: {exc_info}")
        raise exc_info

    else:
        return chat
