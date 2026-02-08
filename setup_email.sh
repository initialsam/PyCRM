#!/bin/bash
# Email 功能快速設定腳本

echo "========================================"
echo "  📧 Email 發送功能設定"
echo "========================================"
echo ""

# 1. 檢查並安裝依賴
echo "📦 1. 檢查 Python 套件..."
if python3 -c "import google.auth" 2>/dev/null; then
    echo "✓ Gmail API 套件已安裝"
else
    echo "⚠️  Gmail API 套件未安裝，開始安裝..."
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
fi

echo ""

# 2. 執行資料庫遷移
echo "🗄️  2. 執行資料庫遷移..."
python3 migrate_email_tables.py

echo ""

# 3. 檢查 credentials.json
echo "🔑 3. 檢查 Gmail API 憑證..."
if [ -f "credentials.json" ]; then
    echo "✓ credentials.json 已存在"
else
    echo "❌ credentials.json 不存在"
    echo ""
    echo "請按照以下步驟設定："
    echo "  1. 前往 https://console.cloud.google.com/"
    echo "  2. 啟用 Gmail API"
    echo "  3. 建立 OAuth 2.0 憑證（Desktop app）"
    echo "  4. 下載 JSON 檔案並重新命名為 credentials.json"
    echo "  5. 將檔案放到專案根目錄"
    echo ""
    echo "詳細說明請參考：EMAIL_SEND_GUIDE.md"
fi

echo ""

# 4. 初始化郵件模板
echo "📝 4. 初始化郵件模板..."
echo "請啟動應用後，執行以下命令："
echo "  curl -X POST http://localhost:8000/api/templates/init"

echo ""
echo "========================================"
echo "  ✅ 設定檢查完成"
echo "========================================"
echo ""
echo "📖 完整使用指南：EMAIL_SEND_GUIDE.md"
echo "🚀 啟動應用：uvicorn app.main:app --reload"
echo ""
