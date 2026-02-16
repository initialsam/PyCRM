"""
匯率查詢路由
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import require_login
from app.exchange_rate import fetch_jpy_rate, save_rate_to_db, get_jpy_rate_history, get_latest_jpy_rate
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# 自訂 Jinja2 過濾器：UTC → 台北時間 (UTC+8)
from datetime import timedelta, timezone as dt_timezone
_TAIPEI_TZ = dt_timezone(timedelta(hours=8))

def _to_taipei(dt_val, fmt="%Y/%m/%d %H:%M"):
    if dt_val is None:
        return ""
    if dt_val.tzinfo is None:
        dt_val = dt_val.replace(tzinfo=dt_timezone.utc)
    return dt_val.astimezone(_TAIPEI_TZ).strftime(fmt)

templates.env.filters["to_taipei"] = _to_taipei


@router.get("/exchange-rate", response_class=HTMLResponse)
async def exchange_rate_page(request: Request, db: Session = Depends(get_db)):
    """歷史匯率查詢頁面"""
    redirect = require_login(request)
    if redirect:
        return redirect

    history = get_jpy_rate_history(db, limit=180)
    latest = get_latest_jpy_rate(db)
    user = request.session.get("user", {})

    # 準備圖表資料（按時間正序）
    chart_dates = [r.rate_date.strftime("%m/%d") + (" 早" if r.period == "morning" else " 晚") for r in reversed(history)]
    chart_values = [r.cash_selling for r in reversed(history)]

    return templates.TemplateResponse(
        "exchange_rate_history.html",
        {
            "request": request,
            "history": history,
            "latest": latest,
            "chart_dates": chart_dates,
            "chart_values": chart_values,
            "user": user,
        },
    )


@router.post("/api/exchange-rate/fetch")
async def fetch_rate_api(request: Request, db: Session = Depends(get_db)):
    """手動觸發爬取匯率"""
    redirect = require_login(request)
    if redirect:
        return JSONResponse({"error": "未登入"}, status_code=401)

    rate_data = fetch_jpy_rate()
    if rate_data:
        save_rate_to_db(db, rate_data)
        return JSONResponse({
            "success": True,
            "rate": rate_data["cash_selling"],
            "date": str(rate_data["rate_date"]),
        })
    else:
        return JSONResponse({"success": False, "error": "爬取失敗"}, status_code=500)
