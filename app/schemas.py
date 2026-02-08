from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    client_name: str
    project_name: str
    email: str
    project_cost: int

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    client_name: Optional[str] = None
    project_name: Optional[str] = None
    email: Optional[str] = None
    project_cost: Optional[int] = None

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
