from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role_id: int
    is_active: bool


class LoginRequest(BaseModel):
    email: str
    password: str
    tenant: str
