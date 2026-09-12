from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from typing import List, Annotated, Dict
from schemas.register import Register
from sqlalchemy.ext.asyncio import AsyncSession
from base import get_db
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from authx import AuthX, AuthXConfig, TokenPayload
from Config import settings
from models import users
import bcrypt
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
from utils import create_access_token
from dependencies import get_current_user
from manager.websocket_manager import manager
import logging 

logger = logging.getLogger(f"chatapp.{__name__}")

BASE = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=BASE / "templates"
)

router = APIRouter()


session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/")
async def get(request: Request):
    return templates.TemplateResponse(
        request,"main.html"
    )

@router.get("/get_active_user_quantity")
async def get_active_user_number():
    print(manager._quantity_of_websockets)
    print(manager.active_connections)
    return {
        "active_users_quantity": manager._quantity_of_websockets
    }

@router.post("/register")
async def registration(data: Register, session: session, response: Response):

    hashed_password = bcrypt.hashpw(
        data.password.get_secret_value().encode("utf-8"), bcrypt.gensalt()
        )

    data = users(
        email=data.email,
        username=data.username,
        password=hashed_password.decode("utf-8"),
        first_name=data.first_name,
        last_name=data.last_name,
    )

    session.add(data)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            401,
            "User exists before :("
        )
    

    access_token: str = create_access_token(data.email)

    # logging.info(f"⚡ACCESS TOKEN: {access_token}")
    print(f"⚡ACCESS TOKEN: {access_token}")


    redirect = RedirectResponse(
        url="/",
        status_code=303
    )
    redirect.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax", secure=True)


    return redirect

@router.post("/open_room")
async def create_room(session:session):
    ...

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session:session,
    current_user: users = Depends(get_current_user)
):
    
    await manager.connect(websocket=websocket)

    join = json.dumps({"user": str(current_user.id), "content": f"{current_user.first_name} joined to the chat"})
    logger.info(str(current_user.id))


    await manager.broadcast(join)
    
    try:
        while True:

            raw = await websocket.receive_text()

            data = json.dumps({"user": str(current_user.id), "content": f"#{current_user.first_name}: {raw}"})

            await manager.broadcast(data)



    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        logger.info(f"#{current_user.first_name} left from the chat!")
        await manager.broadcast(json.dumps({
            "user": str(current_user.id),
            "content": f"#{current_user.first_name} has left the chat"
        }))

    except Exception as e:
        logger.exception("Something happened with exception!")
        await manager.disconnect(websocket)


