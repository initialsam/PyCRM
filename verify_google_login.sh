#!/bin/bash

# Google Login 功能驗證腳本

echo "================================"
echo "Google OAuth 登入功能檢查"
echo "================================"
echo ""

# 檢查必要的套件
echo "1. 檢查 Python 套件..."
uv pip list | grep -E "authlib|itsdangerous|httpx" && echo "✓ 必要套件已安裝" || echo "✗ 缺少必要套件"
echo ""

# 檢查環境變數
echo "2. 檢查環境變數..."
if [ -f .env ]; then
    echo "✓ .env 檔案存在"
    grep -q "GOOGLE_CLIENT_ID" .env && echo "✓ GOOGLE_CLIENT_ID 已設定" || echo "✗ GOOGLE_CLIENT_ID 未設定"
    grep -q "GOOGLE_CLIENT_SECRET" .env && echo "✓ GOOGLE_CLIENT_SECRET 已設定" || echo "✗ GOOGLE_CLIENT_SECRET 未設定"
    grep -q "SECRET_KEY" .env && echo "✓ SECRET_KEY 已設定" || echo "✗ SECRET_KEY 未設定"
else
    echo "✗ .env 檔案不存在"
    echo "  請參考 .env.example 建立 .env 檔案"
fi
echo ""

# 檢查檔案
echo "3. 檢查相關檔案..."
[ -f "app/auth.py" ] && echo "✓ app/auth.py 存在" || echo "✗ app/auth.py 不存在"
[ -f "app/templates/login.html" ] && echo "✓ app/templates/login.html 存在" || echo "✗ app/templates/login.html 不存在"
[ -f "GOOGLE_LOGIN_SETUP.md" ] && echo "✓ GOOGLE_LOGIN_SETUP.md 存在" || echo "✗ GOOGLE_LOGIN_SETUP.md 不存在"
echo ""

# 檢查 main.py 中的認證路由
echo "4. 檢查認證路由..."
grep -q "@app.get(\"/login\"" app/main.py && echo "✓ /login 路由已設定" || echo "✗ /login 路由未設定"
grep -q "@app.get(\"/auth/login\"" app/main.py && echo "✓ /auth/login 路由已設定" || echo "✗ /auth/login 路由未設定"
grep -q "@app.get(\"/auth/callback\"" app/main.py && echo "✓ /auth/callback 路由已設定" || echo "✗ /auth/callback 路由未設定"
grep -q "@app.get(\"/logout\"" app/main.py && echo "✓ /logout 路由已設定" || echo "✗ /logout 路由未設定"
echo ""

echo "================================"
echo "檢查完成！"
echo "================================"
echo ""
echo "接下來的步驟："
echo "1. 到 Google Cloud Console 建立 OAuth 憑證"
echo "2. 設定 .env 檔案中的環境變數"
echo "3. 執行: uvicorn app.main:app --reload"
echo "4. 瀏覽器開啟 http://localhost:8000"
echo ""
echo "詳細設定說明請參閱: GOOGLE_LOGIN_SETUP.md"
