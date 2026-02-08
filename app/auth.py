from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def get_allowed_emails():
    """取得允許登入的 email 列表"""
    allowed = os.getenv('ALLOWED_EMAILS', 'helpaction4u@gmail.com')
    emails = [email.strip() for email in allowed.split(',')]
    logger.info(f"允許登入的 email 列表: {emails}")
    return emails

def is_email_allowed(email: str) -> bool:
    """檢查 email 是否在允許的白名單中"""
    if not email:
        logger.warning("嘗試驗證空的 email")
        return False
    
    allowed_emails = get_allowed_emails()
    allowed_emails_lower = [e.lower() for e in allowed_emails]
    is_allowed = email.lower() in allowed_emails_lower
    
    if is_allowed:
        logger.info(f"✓ Email 驗證通過: {email}")
    else:
        logger.warning(f"✗ Email 驗證失敗: {email} (不在白名單中)")
        logger.warning(f"  白名單內容: {allowed_emails}")
        logger.warning(f"  比對結果: {email.lower()} not in {allowed_emails_lower}")
    
    return is_allowed

def get_current_user(request: Request):
    user = request.session.get('user')
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user

def require_login(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)
    return None
