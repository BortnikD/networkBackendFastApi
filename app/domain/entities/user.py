from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    is_active: bool = False
    date_joined: datetime
    last_active_time: datetime
    is_superuser: bool

    class Config:
        from_attributes = True