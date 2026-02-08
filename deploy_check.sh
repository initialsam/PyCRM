#!/bin/bash
echo "========================================="
echo "🚀 Zeabur 部署前檢查"
echo "========================================="
echo ""

READY=true

echo "1️⃣  檢查必要檔案"
for file in requirements.txt Dockerfile Procfile zeabur.json .env.example; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file 缺失"
        READY=false
    fi
done

echo ""
echo "2️⃣  檢查 requirements.txt"
if grep -q "fastapi" requirements.txt && grep -q "uvicorn" requirements.txt && grep -q "sqlalchemy" requirements.txt; then
    echo "   ✅ 包含必要套件"
else
    echo "   ❌ 缺少必要套件"
    READY=false
fi

echo ""
echo "3️⃣  檢查資料庫配置"
if grep -q "POSTGRES_URL" app/database.py; then
    echo "   ✅ 支援 Zeabur PostgreSQL 環境變數"
else
    echo "   ⚠️  建議添加 POSTGRES_URL 支援"
fi

echo ""
echo "4️⃣  檢查端口配置"
if grep -q "PORT" app/main.py; then
    echo "   ✅ 支援動態端口配置"
else
    echo "   ❌ 未支援動態端口"
    READY=false
fi

echo ""
echo "5️⃣  檢查 .gitignore"
if [ -f ".gitignore" ] && grep -q ".env" .gitignore; then
    echo "   ✅ .gitignore 配置正確"
else
    echo "   ⚠️  建議添加 .env 到 .gitignore"
fi

echo ""
echo "6️⃣  檢查靜態檔案"
if [ -d "app/static" ] && [ -d "app/templates" ]; then
    echo "   ✅ 靜態檔案和模板存在"
else
    echo "   ❌ 缺少靜態檔案或模板"
    READY=false
fi

echo ""
echo "========================================="
if [ "$READY" = true ]; then
    echo "✅ 準備就緒！可以開始部署"
    echo ""
    echo "下一步："
    echo "  1. 推送程式碼到 GitHub"
    echo "  2. 在 Zeabur 建立專案"
    echo "  3. 連接 GitHub repository"
    echo "  4. 添加 PostgreSQL 服務"
    echo "  5. 設定環境變數"
    echo ""
    echo "詳細步驟請參考: cat ZEABUR_DEPLOY.md"
else
    echo "❌ 請先修復上述問題再部署"
fi
echo "========================================="
