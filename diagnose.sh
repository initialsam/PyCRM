#!/bin/bash
# CRM 系統診斷和修復腳本

echo "=========================================="
echo "  🔍 CRM 系統診斷"
echo "=========================================="
echo ""

# 1. 檢查 Python
echo "1️⃣ 檢查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ 未安裝 Python 3"
    exit 1
fi

echo ""

# 2. 檢查依賴套件
echo "2️⃣ 檢查依賴套件..."
MISSING_PACKAGES=()

if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "   ❌ FastAPI 未安裝"
    MISSING_PACKAGES+=("fastapi")
else
    echo "   ✅ FastAPI 已安裝"
fi

if ! python3 -c "import sqlalchemy" 2>/dev/null; then
    echo "   ❌ SQLAlchemy 未安裝"
    MISSING_PACKAGES+=("sqlalchemy")
else
    echo "   ✅ SQLAlchemy 已安裝"
fi

if ! python3 -c "import psycopg2" 2>/dev/null; then
    echo "   ❌ psycopg2 未安裝"
    MISSING_PACKAGES+=("psycopg2")
else
    echo "   ✅ psycopg2 已安裝"
fi

echo ""

# 3. 檢查環境變數
echo "3️⃣ 檢查環境變數..."
if [ -f .env ]; then
    echo "   ✅ .env 檔案存在"
    
    if grep -q "DATABASE_URL" .env; then
        echo "   ✅ DATABASE_URL 已設定"
    else
        echo "   ⚠️  DATABASE_URL 未設定"
    fi
    
    if grep -q "GOOGLE_CLIENT_ID" .env; then
        echo "   ✅ GOOGLE_CLIENT_ID 已設定"
    else
        echo "   ⚠️  GOOGLE_CLIENT_ID 未設定"
    fi
else
    echo "   ❌ .env 檔案不存在"
    echo "   建議：cp .env.example .env"
fi

echo ""

# 4. 檢查資料庫
echo "4️⃣ 檢查資料庫連線..."
if command -v psql &> /dev/null; then
    echo "   ✅ PostgreSQL 客戶端已安裝"
else
    echo "   ⚠️  PostgreSQL 客戶端未安裝"
fi

echo ""

# 5. 提供修復建議
if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "=========================================="
    echo "  🔧 需要修復"
    echo "=========================================="
    echo ""
    echo "發現 ${#MISSING_PACKAGES[@]} 個未安裝的套件"
    echo ""
    echo "💡 修復方案 1（使用 pip）："
    echo "   pip install -r requirements.txt"
    echo ""
    echo "💡 修復方案 2（使用 uv）："
    echo "   uv pip install -r requirements.txt"
    echo ""
    read -p "是否現在安裝依賴套件？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "開始安裝..."
        if command -v uv &> /dev/null; then
            uv pip install -r requirements.txt
        else
            pip install -r requirements.txt
        fi
        echo "✅ 安裝完成！"
    fi
else
    echo "=========================================="
    echo "  ✅ 系統檢查完成"
    echo "=========================================="
    echo ""
    echo "所有依賴套件已安裝！"
    echo ""
    echo "🚀 啟動應用："
    echo "   uvicorn app.main:app --reload"
    echo ""
    echo "或使用 uv："
    echo "   uv run uvicorn app.main:app --reload"
fi

echo ""
echo "=========================================="
echo "  📖 相關文件"
echo "=========================================="
echo "   - README.md - 完整說明"
echo "   - QUICKSTART.md - 快速開始"
echo "   - EMAIL_SEND_GUIDE.md - Email 功能"
echo ""
