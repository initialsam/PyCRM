#!/usr/bin/env python3
"""初始化郵件模板到資料庫"""

import sys
sys.path.append('.')

from app.database import SessionLocal, engine
from app.models import EmailTemplate, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

def init_email_templates():
    db = SessionLocal()
    
    try:
        # 檢查是否已有模板
        existing_count = db.query(EmailTemplate).count()
        if existing_count > 0:
            print(f"✓ 已有 {existing_count} 個模板存在")
            
            # 顯示現有模板
            templates = db.query(EmailTemplate).all()
            for t in templates:
                print(f"  - {t.name} ({t.template_type})")
            return
        
        # 建立預設模板
        default_templates = [
            {
                "name": "請款單",
                "template_type": "invoice",
                "subject": "【請款通知】{{project_name}} 專案款項",
                "content": """<!DOCTYPE html>
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
</html>""",
                "is_active": True
            },
            {
                "name": "中秋節問候",
                "template_type": "greeting",
                "subject": "🌕 中秋佳節愉快！",
                "content": """<!DOCTYPE html>
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
</html>""",
                "is_active": True
            },
            {
                "name": "周年慶優惠",
                "template_type": "promotion",
                "subject": "🎉 周年慶特惠活動 - 限時優惠！",
                "content": """<!DOCTYPE html>
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
</html>""",
                "is_active": True
            }
        ]
        
        print("建立郵件模板...")
        for tmpl_data in default_templates:
            template = EmailTemplate(**tmpl_data)
            db.add(template)
            print(f"  ✓ {tmpl_data['name']}")
        
        db.commit()
        print(f"\n✅ 成功建立 {len(default_templates)} 個郵件模板！")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("========================================")
    print("初始化郵件模板")
    print("========================================")
    print()
    
    init_email_templates()
    
    print()
    print("========================================")
    print("完成！")
    print("========================================")
