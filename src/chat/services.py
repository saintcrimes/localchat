from sqlalchemy.ext.asyncio import AsyncSession
from models import users as User, Chat, ChatType
from sqlalchemy import select, and_
from uuid import UUID


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

    return result
