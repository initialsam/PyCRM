"""
資料庫遷移腳本：新增 EmailTemplate 和 EmailLog 表
"""
from sqlalchemy import create_engine
from app.database import Base, engine
from app.models import Client, EmailTemplate, EmailLog
import os

def migrate_database():
    """執行資料庫遷移"""
    print("🔄 開始資料庫遷移...")
    
    try:
        # 建立所有新表（如果不存在）
        Base.metadata.create_all(bind=engine)
        print("✅ 資料庫表已建立/更新")
        
        # 驗證表是否存在
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 現有資料表：")
        for table in tables:
            print(f"  - {table}")
        
        required_tables = ['clients', 'email_templates', 'email_logs']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n⚠️  缺少資料表：{', '.join(missing_tables)}")
            return False
        else:
            print(f"\n✅ 所有必要資料表都已建立")
            return True
            
    except Exception as e:
        print(f"❌ 遷移失敗：{e}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    if success:
        print("\n🎉 資料庫遷移完成！")
        print("\n📝 下一步：")
        print("  1. 初始化郵件模板：POST /api/templates/init")
        print("  2. 下載 Gmail API credentials.json")
        print("  3. 開始使用郵件發送功能")
    else:
        print("\n⚠️  請檢查錯誤訊息並重試")
