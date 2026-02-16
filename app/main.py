from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.routers import clients, emails, exchange_rate as exchange_rate_router
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

# 信任 proxy headers（Zeabur 在 proxy 後面）
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["pycrm.zeabur.app", "*.zeabur.app", "localhost", "127.0.0.1"]
)

# 配置 Session Middleware - 修復 OAuth state 匹配問題
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    session_cookie="session",
    max_age=3600,  # 1 hour
    same_site="none",  # 允許跨站點，OAuth redirect 需要
    https_only=True,   # Zeabur 使用 HTTPS，必須設為 True
    path="/"           # 整個網站可用
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 自訂 Jinja2 過濾器：UTC → 台北時間 (UTC+8)
from datetime import timedelta, timezone as dt_timezone
_TAIPEI_TZ = dt_timezone(timedelta(hours=8))

def _to_taipei(dt_val, fmt="%Y/%m/%d %H:%M"):
    """將 UTC datetime 轉換為台北時間並格式化"""
    if dt_val is None:
        return ""
    if dt_val.tzinfo is None:
        # 假設 naive datetime 為 UTC
        dt_val = dt_val.replace(tzinfo=dt_timezone.utc)
    return dt_val.astimezone(_TAIPEI_TZ).strftime(fmt)

templates.env.filters["to_taipei"] = _to_taipei

app.include_router(clients.router)
app.include_router(emails.router)
app.include_router(exchange_rate_router.router)

def get_redirect_uri(request: Request, callback_name: str, env_var: str = None) -> str:
    """
    取得正確的 redirect_uri
    
    Args:
        request: FastAPI Request 物件
        callback_name: 回調路由名稱（如 'auth_callback'）
        env_var: 環境變數名稱（如 'OAUTH_REDIRECT_URI'）
    
    Returns:
        正確的 redirect_uri（在 Zeabur 上使用 https）
    """
    # 優先使用環境變數
    if env_var:
        redirect_uri = os.getenv(env_var)
        if redirect_uri:
            logger.info(f"使用環境變數 {env_var}: {redirect_uri}")
            return redirect_uri
    
    # 自動生成
    redirect_uri = str(request.url_for(callback_name))
    
    # 檢查是否在 Zeabur 或其他需要 HTTPS 的環境
    host = request.headers.get('host', '')
    x_forwarded_proto = request.headers.get('x-forwarded-proto', '')
    
    # 如果是 zeabur.app 域名，或者 proxy 指示使用 https，強制使用 https
    if 'zeabur.app' in host or x_forwarded_proto == 'https':
        redirect_uri = redirect_uri.replace('http://', 'https://')
        logger.info(f"檢測到 HTTPS 環境，修正 redirect_uri: {redirect_uri}")
    
    return redirect_uri

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/auth/login")
async def auth_login(request: Request):
    redirect_uri = get_redirect_uri(request, 'auth_callback', 'OAUTH_REDIRECT_URI')
    
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
        
        # authlib 會從 session 中自動恢復 redirect_uri，不需要明確傳遞
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

@app.get("/auth/gmail/login")
async def gmail_auth_login(request: Request):
    """Gmail API 授權登入"""
    redirect_uri = get_redirect_uri(request, 'gmail_auth_callback', 'GMAIL_OAUTH_REDIRECT_URI')
    
    logger.info(f"啟動 Gmail API OAuth 流程，redirect_uri: {redirect_uri}")
    logger.info(f"Request headers - Host: {request.headers.get('host')}, X-Forwarded-Proto: {request.headers.get('x-forwarded-proto')}")
    logger.info(f"Session ID before: {request.session.get('_id', 'no session')}")
    logger.info(f"Session data before: {dict(request.session)}")
    
    return await oauth.google_gmail.authorize_redirect(
        request, 
        redirect_uri,
        access_type='offline',
        prompt='consent'
    )

@app.get("/auth/gmail/callback")
async def gmail_auth_callback(request: Request):
    """Gmail API OAuth 回調"""
    try:
        logger.info("開始處理 Gmail OAuth 回調")
        logger.info(f"Callback URL: {request.url}")
        logger.info(f"Request headers - Host: {request.headers.get('host')}, X-Forwarded-Proto: {request.headers.get('x-forwarded-proto')}")
        logger.info(f"Session ID after: {request.session.get('_id', 'no session')}")
        logger.info(f"Session data after: {dict(request.session)}")
        logger.info(f"Session keys: {list(request.session.keys())}")
        
        # authlib 會從 session 中自動恢復 redirect_uri，不需要明確傳遞
        token = await oauth.google_gmail.authorize_access_token(request)
        
        # 儲存 Gmail token 到 session
        request.session['gmail_token'] = {
            'access_token': token.get('access_token'),
            'refresh_token': token.get('refresh_token'),
            'token_type': token.get('token_type'),
            'expires_in': token.get('expires_in')
        }
        
        logger.info("✓ Gmail API 授權成功")
        
        return templates.TemplateResponse("gmail_auth_success.html", {
            "request": request
        })
    except Exception as e:
        logger.error(f"Gmail OAuth 回調發生異常: {type(e).__name__}: {str(e)}", exc_info=True)
        return templates.TemplateResponse("gmail_auth_error.html", {
            "request": request,
            "error": str(e)
        })

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

    # 取得最新日幣匯率
    from app.exchange_rate import get_latest_jpy_rate
    jpy_rate = get_latest_jpy_rate(db)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "clients": clients_list,
            "stats": stats,
            "search": search or "",
            "user": user,
            "jpy_rate": jpy_rate,
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

# === APScheduler: 每天早上 8:00 + 晚上 20:00 自動爬取日幣匯率 ===
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def scheduled_fetch_rate():
    """排程任務：爬取日幣匯率並存入資料庫"""
    from app.exchange_rate import fetch_and_save
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        success = fetch_and_save(db)
        if success:
            logger.info("✓ 排程爬取日幣匯率成功")
        else:
            logger.error("✗ 排程爬取日幣匯率失敗")
    except Exception as e:
        logger.error(f"排程爬取匯率時發生錯誤: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduled_fetch_rate,
    CronTrigger(hour=8, minute=0, timezone="Asia/Taipei"),
    id="fetch_jpy_rate_morning",
    name="每日早上8點爬取日幣匯率",
    replace_existing=True,
)
scheduler.add_job(
    scheduled_fetch_rate,
    CronTrigger(hour=20, minute=0, timezone="Asia/Taipei"),
    id="fetch_jpy_rate_evening",
    name="每日晚上8點爬取日幣匯率",
    replace_existing=True,
)
scheduler.start()
logger.info("✓ APScheduler 已啟動：每日 08:00 / 20:00 (Asia/Taipei) 爬取日幣匯率")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
