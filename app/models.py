from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    project_cost = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 模板名稱
    subject = Column(String, nullable=False)  # 郵件主旨
    content = Column(Text, nullable=False)  # 郵件內容 (支援 HTML)
    template_type = Column(String, nullable=False)  # 類型: invoice, greeting, promotion
    is_active = Column(Boolean, default=True)  # 是否啟用
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)  # 收件客戶 ID
    client_email = Column(String, nullable=False)  # 收件 email
    template_id = Column(Integer, nullable=True)  # 使用的模板 ID
    subject = Column(String, nullable=False)  # 郵件主旨
    status = Column(String, default='pending')  # 狀態: pending, sent, failed
    error_message = Column(Text, nullable=True)  # 錯誤訊息
    sent_at = Column(DateTime(timezone=True), nullable=True)  # 發送時間
    created_at = Column(DateTime(timezone=True), server_default=func.now())
