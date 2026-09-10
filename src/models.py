from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Enum as SAEnum, DateTime, Index
from .base import Base, metadata
from datetime import datetime, timezone
from typing import List, Optional
import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID

class RoomRole(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    member = "member"


class MessageType(enum.Enum):
    TEXT = "text"
    FILE = "file"

class ChatType(enum.Enum):
    DIRECT = "direct"
    GROUP = "group"

chat_participant = Table(
    "chat_participant",
    metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("chat_id", ForeignKey("chat.id"), primary_key=True)
)

class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    chat_type: Mapped[str] = mapped_column(SAEnum(ChatType,inherit_schema=True))

    users: Mapped[List["users"]] = relationship(secondary=chat_participant,  back_populates="chats")
    read_statuses: Mapped[List["ReadStatus"]] = relationship(back_populates="chat")


class users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    user_image: Mapped[Optional[str]] = mapped_column(String(1028), nullable=True)


    chats: Mapped[List["Chat"]] = relationship(secondary=chat_participant,  back_populates="users")
    messages : Mapped[List["messages"]] = relationship(back_populates="sender")
    read_statuses: Mapped[List["ReadStatus"]] = relationship(back_populates="user")

    
class messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    senderId: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chatId: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    content: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False) 

    
    sender: Mapped["users"] = relationship(back_populates="messages")


class ReadStatus(Base):
    __tablename__ = "readstatus"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_read_message_id: Mapped[int] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))


    chat: Mapped["Chat"] = relationship(back_populates="read_statuses")
    user: Mapped["users"] = relationship(back_populates="read_statuses")

    __table_args__ = (
        Index("idx_read_status_on_chat_id", "chat_id"),
        Index("idx_read_status_on_user_id", "user_id"),
    )