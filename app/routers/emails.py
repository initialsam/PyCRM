from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import require_login
from app.email_service import gmail_service
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/send-email", response_class=HTMLResponse)
async def send_email_page(request: Request, db: Session = Depends(get_db)):
    """郵件發送頁面"""
    login_check = require_login(request)
    if login_check:
        return login_check
    
    # 檢查 Gmail API 是否已授權
    is_gmail_auth = gmail_service.is_authenticated()
    
    # 取得所有客戶
    clients = db.query(models.Client).all()
    
    # 取得所有啟用的模板
    templates_list = db.query(models.EmailTemplate).filter(
        models.EmailTemplate.is_active == True
    ).all()
    
    return templates.TemplateResponse("send_email.html", {
        "request": request,
        "clients": clients,
        "templates": templates_list,
        "is_gmail_auth": is_gmail_auth
    })

@router.post("/api/emails/send")
async def send_emails(
    request: Request,
    email_request: schemas.EmailSendRequest,
    db: Session = Depends(get_db)
):
    """發送郵件 API"""
    login_check = require_login(request)
    if login_check:
        raise HTTPException(status_code=401, detail="未登入")
    
    # 取得模板
    template = db.query(models.EmailTemplate).filter(
        models.EmailTemplate.id == email_request.template_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="找不到郵件模板")
    
    # 取得客戶
    clients = db.query(models.Client).filter(
        models.Client.id.in_(email_request.client_ids)
    ).all()
    
    if not clients:
        raise HTTPException(status_code=404, detail="找不到選擇的客戶")
    
    # 發送郵件
    results = []
    for client in clients:
        # 渲染模板
        variables = {
            'client_name': client.client_name,
            'project_name': client.project_name,
            'project_cost': f"NT$ {client.project_cost:,}",
        }
        
        content = gmail_service.render_template(template.content, variables)
        
        # 發送
        result = gmail_service.send_email(
            to=client.email,
            subject=template.subject,
            message_html=content
        )
        
        # 檢查是否需要授權
        if result.get('needs_auth'):
            raise HTTPException(
                status_code=401, 
                detail="Gmail API 未授權，請先完成授權"
            )
        
        # 記錄發送狀態
        log = models.EmailLog(
            client_id=client.id,
            client_email=client.email,
            template_id=template.id,
            subject=template.subject,
            status='sent' if result['success'] else 'failed',
            error_message=result.get('error'),
            sent_at=datetime.now() if result['success'] else None
        )
        db.add(log)
        results.append({
            'client_name': client.client_name,
            'email': client.email,
            'success': result['success'],
            'error': result.get('error')
        })
    
    db.commit()
    
    return {
        'message': '郵件發送完成',
        'results': results,
        'total': len(results),
        'success_count': sum(1 for r in results if r['success']),
        'failed_count': sum(1 for r in results if not r['success'])
    }

@router.get("/email-logs", response_class=HTMLResponse)
async def email_logs_page(request: Request, db: Session = Depends(get_db)):
    """郵件發送記錄頁面"""
    login_check = require_login(request)
    if login_check:
        return login_check
    
    logs = db.query(models.EmailLog).order_by(
        models.EmailLog.created_at.desc()
    ).limit(100).all()
    
    return templates.TemplateResponse("email_logs.html", {
        "request": request,
        "logs": logs
    })

@router.get("/api/templates")
async def get_templates(request: Request, db: Session = Depends(get_db)):
    """取得郵件模板 API"""
    templates = db.query(models.EmailTemplate).filter(
        models.EmailTemplate.is_active == True
    ).all()
    return templates

@router.post("/api/templates/init")
async def init_templates(request: Request, db: Session = Depends(get_db)):
    """初始化預設郵件模板"""
    login_check = require_login(request)
    if login_check:
        raise HTTPException(status_code=401, detail="未登入")
    
    # 檢查是否已有模板
    existing = db.query(models.EmailTemplate).count()
    if existing > 0:
        return {"message": "模板已存在", "count": existing}
    
    # 建立預設模板
    default_templates = [
        {
            "name": "請款單",
            "template_type": "invoice",
            "subject": "【請款通知】{{project_name}} 專案款項",
            "content": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .amount { font-size: 24px; color: #4CAF50; font-weight: bold; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>請款通知</h1>
        </div>
        <div class="content">
            <p>親愛的 <strong>{{client_name}}</strong> 您好，</p>
            <p>關於 <strong>{{project_name}}</strong> 專案，請款金額如下：</p>
            <p class="amount">{{project_cost}}</p>
            <p>請於收到本通知後 7 個工作天內完成付款。</p>
            <p>如有任何問題，請隨時與我們聯繫。</p>
            <p>謝謝您的配合！</p>
        </div>
        <div class="footer">
            <p>此為系統自動發送郵件，請勿直接回覆</p>
        </div>
    </div>
</body>
</html>
            """
        },
        {
            "name": "中秋節問候",
            "template_type": "greeting",
            "subject": "🌕 中秋佳節愉快！",
            "content": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%); 
                  color: white; padding: 30px; text-align: center; }
        .content { padding: 20px; background: #fff; }
        .moon { font-size: 60px; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="moon">🌕</div>
            <h1>中秋佳節愉快</h1>
        </div>
        <div class="content">
            <p>親愛的 <strong>{{client_name}}</strong> 您好，</p>
            <p>中秋佳節將至，感謝您一直以來對我們的支持與信任。</p>
            <p>在此祝福您：</p>
            <ul>
                <li>🌕 人圓、月圓、事事圓滿</li>
                <li>🎑 花好、月好、心情更好</li>
                <li>🥮 餅香、酒香、闔家安康</li>
            </ul>
            <p>期待未來能繼續與您合作！</p>
            <p>祝您中秋節快樂！</p>
        </div>
        <div class="footer">
            <p>敬祝 佳節愉快</p>
        </div>
    </div>
</body>
</html>
            """
        },
        {
            "name": "周年慶優惠",
            "template_type": "promotion",
            "subject": "🎉 周年慶特惠活動 - 限時優惠！",
            "content": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 30px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .discount { background: #FF6B6B; color: white; padding: 15px; 
                   text-align: center; font-size: 28px; font-weight: bold; 
                   border-radius: 10px; margin: 20px 0; }
        .benefits { background: white; padding: 15px; border-left: 4px solid #667eea; margin: 10px 0; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 周年慶特惠活動</h1>
            <p>感恩回饋，限時優惠！</p>
        </div>
        <div class="content">
            <p>親愛的 <strong>{{client_name}}</strong> 您好，</p>
            <p>我們即將迎來周年慶，為了感謝您的長期支持，特別推出超值優惠方案：</p>
            
            <div class="discount">
                全面 8 折優惠！
            </div>
            
            <div class="benefits">
                <h3>🎁 專屬優惠內容：</h3>
                <ul>
                    <li>新專案合約享 8 折優惠</li>
                    <li>免費技術諮詢服務</li>
                    <li>優先排程安排</li>
                    <li>延長保固期限</li>
                </ul>
            </div>
            
            <p><strong>活動期間：</strong>即日起至月底</p>
            <p>名額有限，欲購從速！歡迎隨時與我們聯繫。</p>
        </div>
        <div class="footer">
            <p>把握機會，立即行動！</p>
        </div>
    </div>
</body>
</html>
            """
        }
    ]
    
    for tmpl_data in default_templates:
        template = models.EmailTemplate(**tmpl_data)
        db.add(template)
    
    db.commit()
    
    return {
        "message": "預設模板已建立",
        "count": len(default_templates)
    }

@router.get("/gmail/auth-url")
async def get_gmail_auth_url(request: Request):
    """取得 Gmail API 授權 URL"""
    login_check = require_login(request)
    if login_check:
        raise HTTPException(status_code=401, detail="未登入")
    
    try:
        auth_url = gmail_service.get_auth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/auth/gmail/callback")
async def gmail_auth_callback(request: Request, code: str = None, error: str = None):
    """Gmail OAuth 回調"""
    if error:
        return templates.TemplateResponse("gmail_auth_error.html", {
            "request": request,
            "error": error
        })
    
    if not code:
        raise HTTPException(status_code=400, detail="缺少授權碼")
    
    try:
        gmail_service.save_credentials(code)
        return templates.TemplateResponse("gmail_auth_success.html", {
            "request": request
        })
    except Exception as e:
        return templates.TemplateResponse("gmail_auth_error.html", {
            "request": request,
            "error": str(e)
        })

@router.get("/gmail/status")
async def gmail_auth_status(request: Request):
    """檢查 Gmail API 授權狀態"""
    login_check = require_login(request)
    if login_check:
        raise HTTPException(status_code=401, detail="未登入")
    
    return {
        "is_authenticated": gmail_service.is_authenticated()
    }
