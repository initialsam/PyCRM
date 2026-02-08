#!/bin/bash
# Email 功能完整測試腳本

echo "========================================"
echo "  📧 Email 功能測試"
echo "========================================"
echo ""

# 1. 檢查檔案結構
echo "📁 1. 檢查檔案..."
files=(
    "app/email_service.py"
    "app/routers/emails.py"
    "app/templates/send_email.html"
    "app/templates/email_logs.html"
    "migrate_email_tables.py"
    "EMAIL_SEND_GUIDE.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (缺少)"
    fi
done

echo ""

# 2. 檢查語法
echo "🔍 2. 檢查 Python 語法..."
python3 -c "import ast; ast.parse(open('app/models.py').read())" && echo "  ✓ models.py" || echo "  ✗ models.py"
python3 -c "import ast; ast.parse(open('app/schemas.py').read())" && echo "  ✓ schemas.py" || echo "  ✗ schemas.py"
python3 -c "import ast; ast.parse(open('app/email_service.py').read())" && echo "  ✓ email_service.py" || echo "  ✗ email_service.py"
python3 -c "import ast; ast.parse(open('app/routers/emails.py').read())" && echo "  ✓ routers/emails.py" || echo "  ✗ routers/emails.py"

echo ""

# 3. 檢查依賴
echo "📦 3. 檢查依賴套件..."
grep -q "google-auth" requirements.txt && echo "  ✓ google-auth" || echo "  ✗ google-auth (缺少)"
grep -q "google-api-python-client" requirements.txt && echo "  ✓ google-api-python-client" || echo "  ✗ google-api-python-client (缺少)"

echo ""

# 4. 檢查 main.py 整合
echo "🔗 4. 檢查路由整合..."
if grep -q "from app.routers import clients, emails" app/main.py; then
    echo "  ✓ emails router 已匯入"
else
    echo "  ✗ emails router 未匯入"
fi

if grep -q "app.include_router(emails.router)" app/main.py; then
    echo "  ✓ emails router 已註冊"
else
    echo "  ✗ emails router 未註冊"
fi

echo ""

# 5. 檢查 dashboard 整合
echo "🎨 5. 檢查 Dashboard 整合..."
if grep -q "send-email" app/templates/dashboard.html; then
    echo "  ✓ 發送郵件按鈕已加入"
else
    echo "  ✗ 發送郵件按鈕未加入"
fi

if grep -q "email-logs" app/templates/dashboard.html; then
    echo "  ✓ 發送記錄按鈕已加入"
else
    echo "  ✗ 發送記錄按鈕未加入"
fi

echo ""

# 6. 檢查 credentials
echo "🔑 6. 檢查 Gmail API 憑證..."
if [ -f "credentials.json" ]; then
    echo "  ✓ credentials.json 存在"
else
    echo "  ⚠️  credentials.json 不存在（首次使用需要設定）"
fi

echo ""
echo "========================================"
echo "  測試完成"
echo "========================================"
echo ""
echo "📝 下一步："
echo "  1. 安裝依賴：pip install -r requirements.txt"
echo "  2. 執行遷移：python3 migrate_email_tables.py"
echo "  3. 啟動應用：uvicorn app.main:app --reload"
echo "  4. 初始化模板：curl -X POST http://localhost:8000/api/templates/init"
echo "  5. 設定 Gmail API：參考 EMAIL_SEND_GUIDE.md"
echo ""
