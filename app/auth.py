from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import os

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
    return [email.strip() for email in allowed.split(',')]

def is_email_allowed(email: str) -> bool:
    """檢查 email 是否在允許的白名單中"""
    if not email:
        return False
    allowed_emails = get_allowed_emails()
    return email.lower() in [e.lower() for e in allowed_emails]

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
