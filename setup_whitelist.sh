#!/bin/bash
# Email 白名單快速設定腳本

echo "========================================"
echo "  Email 白名單帳號管理系統"
echo "========================================"
echo ""

# 檢查 .env 檔案
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 檔案，從範例建立..."
    cp .env.example .env
fi

# 檢查 ALLOWED_EMAILS
if grep -q "^ALLOWED_EMAILS=" .env; then
    echo "✓ ALLOWED_EMAILS 已設定："
    grep "^ALLOWED_EMAILS=" .env
else
    echo "⚠️  ALLOWED_EMAILS 未設定，新增預設值..."
    echo "" >> .env
    echo "# 允許登入的 Email 白名單" >> .env
    echo "ALLOWED_EMAILS=helpaction4u@gmail.com" >> .env
    echo "✓ 已新增 ALLOWED_EMAILS=helpaction4u@gmail.com"
fi

echo ""
echo "========================================"
echo "  設定完成！"
echo "========================================"
echo ""
echo "📋 如何新增更多帳號："
echo "   編輯 .env 檔案，修改 ALLOWED_EMAILS，用逗號分隔"
echo "   範例：ALLOWED_EMAILS=email1@gmail.com,email2@gmail.com"
echo ""
echo "🚀 Zeabur 部署："
echo "   在 Zeabur Dashboard 設定環境變數 ALLOWED_EMAILS"
echo ""
echo "📖 詳細說明請參考：EMAIL_WHITELIST.md"
echo ""
