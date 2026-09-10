from fastapi import APIRouter, Depends
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

logger = logging.getLogger(__name__)

chat_router = APIRouter(tags=["Chat Management"])

session = Annotated[AsyncSession, Depends(get_db)]

@chat_router.post(
        "/chat/direct_chat",
        dependencies=[
            Depends(RateLimiter(limiter=Limiter(Rate(50, Duration.HOUR * 24)))),
            Depends(RateLimiter(limiter=Limiter(Rate(10, Duration.MINUTE * 1)))),
        ],
        summary="Register"
)
async def create_direct_chat(
    create_direct_chat_schema: CreateDirectChatSchema,
    db_session: session,
    response: Response,
):  

    recipient_user = create_direct_chat_schema.recipient_user_guid

    return recipient_user

        
    