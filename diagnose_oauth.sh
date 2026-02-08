#!/bin/bash
# OAuth Session 診斷工具

echo "========================================="
echo "OAuth Session 配置診斷"
echo "========================================="
echo ""

# 檢查關鍵配置
echo "📋 檢查 app/main.py 配置..."
echo ""

echo "1. SessionMiddleware 配置:"
grep -A 7 "SessionMiddleware," app/main.py | grep -E "same_site|https_only|max_age|session_cookie"
echo ""

echo "2. TrustedHostMiddleware:"
if grep -q "TrustedHostMiddleware" app/main.py; then
    echo "   ✅ 已配置 TrustedHostMiddleware"
else
    echo "   ❌ 未配置 TrustedHostMiddleware"
fi
echo ""

echo "3. get_redirect_uri 函數:"
if grep -q "def get_redirect_uri" app/main.py; then
    echo "   ✅ 已定義 get_redirect_uri"
else
    echo "   ❌ 未定義 get_redirect_uri"
fi
echo ""

# 檢查環境變數
echo "🔧 環境變數檢查..."
echo ""

check_env() {
    if [ -z "${!1}" ]; then
        echo "   ❌ $1 未設定"
        return 1
    else
        echo "   ✅ $1 已設定"
        return 0
    fi
}

check_env "SECRET_KEY"
check_env "GOOGLE_CLIENT_ID"
check_env "GOOGLE_CLIENT_SECRET"
check_env "ALLOWED_EMAILS"
echo ""
check_env "OAUTH_REDIRECT_URI"
check_env "GMAIL_OAUTH_REDIRECT_URI"
echo ""

# 檢查語法
echo "🐍 Python 語法檢查..."
python -m py_compile app/main.py app/auth.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 語法檢查通過"
else
    echo "❌ 語法錯誤"
    exit 1
fi
echo ""

# 提供建議
echo "========================================="
echo "📝 配置建議"
echo "========================================="
echo ""
echo "當前配置應該："
echo "  ✅ same_site='none' （允許 OAuth redirect）"
echo "  ✅ https_only=True （Zeabur HTTPS 環境）"
echo "  ✅ TrustedHostMiddleware （處理 proxy headers）"
echo ""
echo "如果還是有問題，檢查："
echo "  1. 清除瀏覽器所有 cookies"
echo "  2. 使用無痕模式測試"
echo "  3. 檢查 Zeabur 日誌中的 Session ID"
echo "  4. 確認 SECRET_KEY 不為空且沒有改變"
echo ""

echo "========================================="
echo "🧪 測試步驟"
echo "========================================="
echo ""
echo "1. 重啟應用（Zeabur 會自動部署）"
echo "2. 完全清除瀏覽器 cookies"
echo "3. 訪問 https://pycrm.zeabur.app/login"
echo "4. 登入成功後，訪問 /send-email"
echo "5. 點擊「授權 Gmail API」"
echo "6. 檢查 Zeabur 日誌："
echo "   - Session ID before 和 after 應該一致"
echo "   - 應該看到 '✓ Gmail API 授權成功'"
echo ""

echo "========================================="
echo "📚 相關文件"
echo "========================================="
echo ""
echo "  - SESSION_COOKIE_FIX.md - 詳細說明"
echo "  - OAUTH_COMPLETE_GUIDE.md - 完整指南"
echo "  - OAUTH_FLOW_DIAGRAM.md - 流程圖"
echo ""
