from uuid import UUID
from pydantic import BaseModel


class LoginSchema(BaseModel):
    phone_number: str

class RefreshLoginSchema(BaseModel):
    refresh_token: str

class ResponseTokensSchema(BaseModel):
    user_id: UUID
    access_token: str
    refresh_token: str
