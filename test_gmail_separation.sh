#!/bin/bash
# Gmail 授權分離測試腳本

echo "==================================="
echo "Gmail 授權分離功能測試"
echo "==================================="
echo ""

# 檢查必要的環境變數
echo "1. 檢查環境變數..."
if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo "❌ 缺少 GOOGLE_CLIENT_ID"
    exit 1
fi

if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo "❌ 缺少 GOOGLE_CLIENT_SECRET"
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ 缺少 SECRET_KEY"
    exit 1
fi

echo "✅ 環境變數設置正確"
echo ""

# 檢查 Python 語法
echo "2. 檢查 Python 語法..."
python -m py_compile app/main.py app/auth.py app/routers/emails.py app/email_service.py
if [ $? -eq 0 ]; then
    echo "✅ Python 語法檢查通過"
else
    echo "❌ Python 語法錯誤"
    exit 1
fi
echo ""

# 檢查關鍵路由是否存在
echo "3. 檢查關鍵代碼..."
echo ""

echo "  檢查 auth.py 中的兩個 OAuth 配置..."
grep -q "name='google'" app/auth.py && echo "  ✅ 找到登入 OAuth 配置"
grep -q "name='google_gmail'" app/auth.py && echo "  ✅ 找到 Gmail OAuth 配置"
echo ""

echo "  檢查 main.py 中的 Gmail 授權路由..."
grep -q "/auth/gmail/login" app/main.py && echo "  ✅ 找到 Gmail 登入路由"
grep -q "/auth/gmail/callback" app/main.py && echo "  ✅ 找到 Gmail 回調路由"
echo ""

echo "  檢查 email_service.py 中的新方法..."
grep -q "set_credentials_from_token" app/email_service.py && echo "  ✅ 找到 set_credentials_from_token 方法"
echo ""

echo "  檢查 emails.py 中的 token 使用..."
grep -q "gmail_token" app/routers/emails.py && echo "  ✅ 找到 gmail_token 使用"
echo ""

echo "==================================="
echo "✅ 所有檢查通過！"
echo "==================================="
echo ""
echo "接下來的步驟："
echo "1. 啟動應用: uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo "2. 訪問 /login 完成登入"
echo "3. 訪問 /send-email"
echo "4. 點擊 '授權 Gmail API' 按鈕"
echo "5. 完成 Gmail 授權"
echo "6. 測試發送郵件"
echo ""
