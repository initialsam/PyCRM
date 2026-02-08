#!/bin/bash
# CRM 系統啟動（無 reload 模式，更穩定）

echo "=========================================="
echo "  🚀 啟動 CRM 系統（穩定模式）"
echo "=========================================="
echo ""

# 檢查虛擬環境
if [ -d ".venv" ]; then
    echo "✅ 啟動虛擬環境"
    source .venv/bin/activate
fi

echo "啟動應用（無 reload 模式）..."
echo ""
echo "訪問："
echo "  - http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止"
echo ""

# 不使用 reload，避免所有 multiprocessing 問題
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info
