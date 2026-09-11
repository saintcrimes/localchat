from fastapi import APIRouter, Depends, status, HTTPException
from .schemas import CreateDirectChatSchema
from base import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user
from models import users as User
from chat.services import direct_chat_exists
import logging
import jwt
from fastapi_limiter.depends import RateLimiter
from fastapi import Response
from pyrate_limiter import Duration, Limiter, Rate
from authentication.services import get_user_guid_by_username
from .services import get_user_by_guid



logger = logging.getLogger(f"chatapp.{__name__}")

chat_router = APIRouter(tags=["Chat Management"])

session = Annotated[AsyncSession, Depends(get_db)]

@chat_router.post("/chat/direct_chat",summary="Register")
async def create_direct_chat(
    create_direct_chat_schema: CreateDirectChatSchema,
    db_session: session,
    response: Response,
):  

    recipient_user_guid = create_direct_chat_schema.recipient_user_guid

    recipient_user: User | None = await get_user_by_guid(db_session, recipient_user_guid)

    if not recipient_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found guid which provided"
        )

    

@chat_router.get("/chat/direct/", summary="Get user's direct chats")
async def chat_direct_get(username: str, db_session: session):

    guid = await get_user_guid_by_username(username=username, db_session=db_session)

   

    return guid