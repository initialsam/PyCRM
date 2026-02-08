#!/bin/bash
# Zeabur 日志檢查與設定腳本

echo "=========================================="
echo "  🔍 Zeabur 日志設定檢查"
echo "=========================================="
echo ""

# 檢查本地 .env 檔案
if [ -f ".env" ]; then
    echo "📋 本地 .env 檔案檢查："
    echo ""
    
    if grep -q "^PYTHONUNBUFFERED=" .env; then
        echo "  ✅ PYTHONUNBUFFERED 已設定："
        grep "^PYTHONUNBUFFERED=" .env
    else
        echo "  ⚠️  PYTHONUNBUFFERED 未設定"
        echo "     建議新增：PYTHONUNBUFFERED=1"
        read -p "     是否要新增到 .env？ (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "" >> .env
            echo "# Python 日志設定" >> .env
            echo "PYTHONUNBUFFERED=1" >> .env
            echo "  ✓ 已新增到 .env"
        fi
    fi
    
    echo ""
    
    if grep -q "^ALLOWED_EMAILS=" .env; then
        echo "  ✅ ALLOWED_EMAILS 已設定："
        grep "^ALLOWED_EMAILS=" .env
    else
        echo "  ⚠️  ALLOWED_EMAILS 未設定"
    fi
else
    echo "⚠️  找不到 .env 檔案"
    echo "   請複製 .env.example 並填寫設定"
fi

echo ""
echo "=========================================="
echo "  📦 檢查設定檔"
echo "=========================================="
echo ""

# 檢查 Procfile
if [ -f "Procfile" ]; then
    echo "📄 Procfile："
    if grep -q -- "--log-level info" Procfile; then
        echo "  ✅ 包含 --log-level info"
        cat Procfile
    else
        echo "  ⚠️  缺少 --log-level info 參數"
        cat Procfile
    fi
else
    echo "  ❌ 找不到 Procfile"
fi

echo ""

# 檢查 zeabur.json
if [ -f "zeabur.json" ]; then
    echo "📄 zeabur.json："
    if grep -q -- "--log-level info" zeabur.json; then
        echo "  ✅ 包含 --log-level info"
        grep "startCommand" zeabur.json
    else
        echo "  ⚠️  缺少 --log-level info 參數"
        grep "startCommand" zeabur.json
    fi
else
    echo "  ❌ 找不到 zeabur.json"
fi

echo ""
echo "=========================================="
echo "  🧪 測試日志輸出"
echo "=========================================="
echo ""

if [ -d ".venv" ]; then
    echo "執行日志測試..."
    echo ""
    source .venv/bin/activate
    export PYTHONUNBUFFERED=1
    python test_login_log.py 2>&1 | grep -E "(INFO|WARNING|ERROR)" | head -10
    echo ""
    echo "✅ 日志測試完成"
else
    echo "⚠️  找不到 .venv 虛擬環境"
    echo "   請先執行：python -m venv .venv"
fi

echo ""
echo "=========================================="
echo "  📝 Zeabur 部署檢查清單"
echo "=========================================="
echo ""
echo "請確認以下項目已在 Zeabur Dashboard 設定："
echo ""
echo "  [ ] PYTHONUNBUFFERED=1"
echo "  [ ] ALLOWED_EMAILS=your@email.com"
echo "  [ ] GOOGLE_CLIENT_ID=..."
echo "  [ ] GOOGLE_CLIENT_SECRET=..."
echo "  [ ] DATABASE_URL=..."
echo "  [ ] SECRET_KEY=..."
echo ""
echo "設定後記得："
echo "  1. 點擊 'Save' 儲存環境變數"
echo "  2. 點擊 'Redeploy' 重新部署"
echo "  3. 到 'Logs' > 'Runtime Logs' 查看日志"
echo ""
echo "詳細說明請查看："
echo "  📖 ZEABUR_LOGS_SETUP.md"
echo "  📖 LOGIN_LOG.md"
echo ""
