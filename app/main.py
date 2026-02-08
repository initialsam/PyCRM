from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.routers import clients, emails
from app import crud, auth
from app.auth import oauth, require_login
import os
import logging
import sys

# 配置日志 - 确保输出到 stdout 以便在 Zeabur 中显示
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    force=True  # 强制重新配置
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM 專案管理系統")

# 配置 Session Middleware - 修復 OAuth state 匹配問題
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    session_cookie="session",
    max_age=3600,  # 1 hour
    same_site="lax",  # 允許跨站點但限制，適合 OAuth
    https_only=False  # 在開發環境設為 False，生產環境應該是 True
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(clients.router)
app.include_router(emails.router)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/auth/login")
async def auth_login(request: Request):
    # 優先使用環境變數設定的 redirect_uri
    redirect_uri = os.getenv('OAUTH_REDIRECT_URI')
    
    # 如果沒有設定，則使用當前請求的 scheme 生成
    if not redirect_uri:
        redirect_uri = str(request.url_for('auth_callback'))
        # 保持原始 scheme（http 或 https）
    
    logger.info(f"啟動 OAuth 流程，redirect_uri: {redirect_uri}")
    logger.info(f"Session ID: {request.session.get('_id', 'no session id')}")
    
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        logger.info("開始處理 OAuth 回調")
        logger.info(f"Callback URL: {request.url}")
        logger.info(f"Session ID: {request.session.get('_id', 'no session id')}")
        logger.info(f"Session keys: {list(request.session.keys())}")
        
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        
        if user:
            email = user.get('email')
            name = user.get('name', 'Unknown')
            logger.info(f"使用者嘗試登入: {name} ({email})")
            
            if not auth.is_email_allowed(email):
                logger.warning(f"拒絕登入: {email} 不在 ALLOWED_EMAILS 白名單中")
                return templates.TemplateResponse("access_denied.html", {
                    "request": request,
                    "email": email
                })
            
            request.session['user'] = dict(user)
            logger.info(f"✓ 登入成功: {name} ({email})")
        else:
            logger.error("無法從 token 獲取使用者資訊")
            
        return RedirectResponse(url='/dashboard')
    except Exception as e:
        logger.error(f"OAuth 回調發生異常: {type(e).__name__}: {str(e)}", exc_info=True)
        return RedirectResponse(url='/login')

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/login')

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, search: str = None, db: Session = Depends(get_db)):
    redirect = require_login(request)
    if redirect:
        return redirect
    clients_list = crud.get_clients(db, search=search)
    stats = crud.get_statistics(db)
    user = request.session.get('user', {})
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "clients": clients_list,
            "stats": stats,
            "search": search or "",
            "user": user
        }
    )

@app.get("/client/new", response_class=HTMLResponse)
async def new_client_form(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": None, "action": "/api/clients/", "method": "POST"}
    )

@app.get("/client/{client_id}/edit", response_class=HTMLResponse)
async def edit_client_form(request: Request, client_id: int, db: Session = Depends(get_db)):
    redirect = require_login(request)
    if redirect:
        return redirect
    client = crud.get_client(db, client_id)
    if not client:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": client, "action": f"/api/clients/{client_id}", "method": "PUT"}
    )

@app.get("/import", response_class=HTMLResponse)
async def import_page(request: Request):
    redirect = require_login(request)
    if redirect:
        return redirect
    return templates.TemplateResponse("import_csv.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
