#!/bin/bash
# CRM 系統啟動腳本

echo "=========================================="
echo "  🚀 啟動 CRM 系統"
echo "=========================================="
echo ""

# 檢查虛擬環境
if [ -d ".venv" ]; then
    echo "✅ 啟動虛擬環境"
    source .venv/bin/activate
fi

# 檢查依賴
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI 未安裝"
    echo "請執行：pip install -r requirements.txt"
    exit 1
fi

echo "✅ 依賴套件已安裝"
echo ""
echo "啟動應用..."
echo ""
echo "訪問："
echo "  - http://localhost:8000"
echo "  - http://127.0.0.1:8000"
echo ""
echo "按 Ctrl+C 停止"
echo ""

# 使用 --reload-dir 避免 multiprocessing 問題
# 或者不使用 --reload 以獲得更穩定的運行
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app --log-level info
