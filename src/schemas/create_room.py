from pydantic import BaseModel

class create_room(BaseModel):
    room_name: str