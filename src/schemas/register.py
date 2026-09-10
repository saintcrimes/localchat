from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    field_serializer,
    EmailStr
)


class Register(BaseModel):
    username: str = Field(min_length=4, max=10)
    email: EmailStr
    password: SecretStr = Field(min_length=8, max=24)
    first_name: str
    last_name: str


    @field_serializer('password', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()