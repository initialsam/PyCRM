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

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    content: str
    template_type: str  # invoice, greeting, promotion
    is_active: bool = True

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplate(EmailTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EmailSendRequest(BaseModel):
    client_ids: list[int]
    template_id: int

class EmailLogBase(BaseModel):
    client_id: int
    client_email: str
    template_id: Optional[int] = None
    subject: str
    status: str = 'pending'
    error_message: Optional[str] = None

class EmailLog(EmailLogBase):
    id: int
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
