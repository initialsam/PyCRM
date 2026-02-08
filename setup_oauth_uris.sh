#!/bin/bash
# Google OAuth Redirect URI 檢查與設定助手

echo "========================================"
echo "Google OAuth Redirect URI 設定助手"
echo "========================================"
echo ""

# 取得當前部署的域名
DOMAIN="${DOMAIN:-pycrm.zeabur.app}"

echo "📍 檢測到的域名: $DOMAIN"
echo ""

# 顯示需要的 Redirect URIs
echo "✅ 需要在 Google Cloud Console 添加的 Redirect URIs："
echo ""
echo "   1. https://${DOMAIN}/auth/callback"
echo "   2. https://${DOMAIN}/auth/gmail/callback"
echo ""

# 顯示設定步驟
echo "📋 設定步驟："
echo ""
echo "1️⃣  前往 Google Cloud Console："
echo "   https://console.cloud.google.com/apis/credentials"
echo ""
echo "2️⃣  選擇你的 OAuth 2.0 客戶端 ID"
echo ""
echo "3️⃣  在「已授權的重新導向 URI」區段，點擊「+ 新增 URI」"
echo ""
echo "4️⃣  逐一添加以下 URIs："
echo "   ┌─────────────────────────────────────────────────────┐"
echo "   │ https://${DOMAIN}/auth/callback          │"
echo "   └─────────────────────────────────────────────────────┘"
echo ""
echo "   ┌─────────────────────────────────────────────────────┐"
echo "   │ https://${DOMAIN}/auth/gmail/callback   │"
echo "   └─────────────────────────────────────────────────────┘"
echo ""
echo "5️⃣  點擊「儲存」按鈕"
echo ""
echo "6️⃣  等待 5-10 分鐘讓設定生效"
echo ""

# 顯示環境變數建議
echo "🔧 建議設定的環境變數（可選但推薦）："
echo ""
echo "   OAUTH_REDIRECT_URI=https://${DOMAIN}/auth/callback"
echo "   GMAIL_OAUTH_REDIRECT_URI=https://${DOMAIN}/auth/gmail/callback"
echo ""

# 顯示必需的環境變數
echo "⚠️  必需的環境變數："
echo ""
echo "   GOOGLE_CLIENT_ID=<你的 Client ID>"
echo "   GOOGLE_CLIENT_SECRET=<你的 Client Secret>"
echo "   SECRET_KEY=<隨機密鑰>"
echo "   ALLOWED_EMAILS=<允許登入的 email，用逗號分隔>"
echo ""

# 檢查環境變數是否設定
echo "🔍 檢查當前環境變數..."
echo ""

check_env_var() {
    if [ -z "${!1}" ]; then
        echo "   ❌ $1 - 未設定"
        return 1
    else
        echo "   ✅ $1 - 已設定"
        return 0
    fi
}

check_env_var "GOOGLE_CLIENT_ID"
check_env_var "GOOGLE_CLIENT_SECRET"
check_env_var "SECRET_KEY"
check_env_var "ALLOWED_EMAILS"
echo ""
check_env_var "OAUTH_REDIRECT_URI"
check_env_var "GMAIL_OAUTH_REDIRECT_URI"

echo ""
echo "========================================"
echo "📚 更多資訊請參閱："
echo "   - REDIRECT_URI_FIX.md"
echo "   - GMAIL_AUTH_SEPARATION.md"
echo "========================================"
