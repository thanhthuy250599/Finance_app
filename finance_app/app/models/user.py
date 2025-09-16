from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    role: str = "user"
    plan: str = "free"
    timezone: str = "Asia/Ho_Chi_Minh"
    two_fa_enabled: bool = False
    subscription_status: str = "active"
    points: int = 0
    level: str = "Beginner"





