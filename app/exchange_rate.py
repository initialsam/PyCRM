"""
臺灣銀行日幣匯率爬蟲模組
爬取 https://rate.bot.com.tw/xrt?Lang=zh-TW 的日幣現金匯率（本行賣出）
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

# 台北時區 UTC+8
TAIPEI_TZ = timezone(timedelta(hours=8))

logger = logging.getLogger(__name__)

TARGET_URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_jpy_rate() -> dict | None:
    """
    爬取臺灣銀行牌告匯率頁面，取得日幣（JPY）現金匯率-本行賣出。

    Returns:
        dict: {"currency": "JPY", "cash_selling": float, "rate_date": date}
        None: 爬取失敗時
    """
    try:
        resp = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        resp.encoding = "utf-8"

        soup = BeautifulSoup(resp.text, "lxml")
        
        # 找到匯率表格中的所有貨幣列
        rows = soup.select("table.table tbody tr")
        
        for row in rows:
            # 每列的貨幣名稱在 td 裡面的 .visible-phone 或 title 屬性
            currency_cell = row.select_one("td.currency div.visible-phone")
            if not currency_cell:
                continue
            
            currency_text = currency_cell.get_text(strip=True)
            
            if "JPY" not in currency_text:
                continue
            
            # 找到 JPY 列，取得「現金匯率-本行賣出」
            # 表格欄位順序：幣別, 現金買入, 現金賣出, 即期買入, 即期賣出
            tds = row.select("td")
            # 現金賣出在 data-table="本行賣出" 的第一個 td（現金匯率區）
            cash_selling_td = None
            for td in tds:
                data_table = td.get("data-table", "")
                if "本行賣出" in data_table and "現金" in data_table:
                    cash_selling_td = td
                    break
            
            if not cash_selling_td:
                # 備用方案：按位置取第三個 td（index 2 = 現金賣出）
                if len(tds) >= 3:
                    cash_selling_td = tds[2]
            
            if cash_selling_td:
                rate_text = cash_selling_td.get_text(strip=True)
                rate_value = float(rate_text)
                
                logger.info(f"✓ 爬取成功: JPY 現金賣出匯率 = {rate_value}")
                return {
                    "currency": "JPY",
                    "cash_selling": rate_value,
                    "rate_date": datetime.now(TAIPEI_TZ).date(),
                }
        
        logger.error("未找到 JPY 匯率資料")
        return None

    except requests.RequestException as e:
        logger.error(f"爬取匯率失敗（網路錯誤）: {e}")
        return None
    except (ValueError, IndexError) as e:
        logger.error(f"解析匯率資料失敗: {e}")
        return None
    except Exception as e:
        logger.error(f"爬取匯率時發生未預期錯誤: {e}")
        return None


def _get_period() -> str:
    """根據當前時間返回 'morning' 或 'evening'"""
    return "morning" if datetime.now(TAIPEI_TZ).hour < 14 else "evening"


def save_rate_to_db(db: Session, rate_data: dict):
    """將匯率資料存入資料庫（一天可存兩筆：早上/晚上）"""
    from app.models import ExchangeRate

    now = datetime.now(timezone.utc)  # DB 存 UTC，前端顯示再轉 UTC+8
    period = _get_period()

    # 檢查同天同時段是否已有資料，有則更新
    existing = (
        db.query(ExchangeRate)
        .filter(
            ExchangeRate.currency == rate_data["currency"],
            ExchangeRate.rate_date == rate_data["rate_date"],
            ExchangeRate.period == period,
        )
        .first()
    )

    if existing:
        existing.cash_selling = rate_data["cash_selling"]
        existing.fetched_at = now
        logger.info(f"更新既有匯率記錄: {rate_data['rate_date']} {period} = {rate_data['cash_selling']}")
    else:
        record = ExchangeRate(
            currency=rate_data["currency"],
            cash_selling=rate_data["cash_selling"],
            rate_date=rate_data["rate_date"],
            period=period,
            fetched_at=now,
        )
        db.add(record)
        logger.info(f"新增匯率記錄: {rate_data['rate_date']} {period} = {rate_data['cash_selling']}")

    db.commit()


def get_latest_jpy_rate(db: Session):
    """查詢最新一筆日幣匯率"""
    from app.models import ExchangeRate

    return (
        db.query(ExchangeRate)
        .filter(ExchangeRate.currency == "JPY")
        .order_by(desc(ExchangeRate.fetched_at))
        .first()
    )


def get_jpy_rate_history(db: Session, limit: int = 180):
    """查詢日幣匯率歷史記錄（一天兩筆，預設 180 筆 = 約 90 天）"""
    from app.models import ExchangeRate

    return (
        db.query(ExchangeRate)
        .filter(ExchangeRate.currency == "JPY")
        .order_by(desc(ExchangeRate.fetched_at))
        .limit(limit)
        .all()
    )


def fetch_and_save(db: Session) -> bool:
    """爬取並儲存匯率（排程任務用）"""
    rate_data = fetch_jpy_rate()
    if rate_data:
        save_rate_to_db(db, rate_data)
        return True
    return False
