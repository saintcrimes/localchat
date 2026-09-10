from pydantic import BaseModel, EmailStr, Field

class AuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8) 