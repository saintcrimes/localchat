from pydantic import BaseModel, UUID4

class CreateDirectChatSchema(BaseModel):
    recipient_user_guid: UUID4

