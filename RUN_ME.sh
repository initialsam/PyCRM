#!/bin/bash
# 最簡單的啟動方式 - 無任何複雜選項

clear
echo "=========================================="
echo "  🚀 CRM 系統啟動"
echo "=========================================="
echo ""

# 進入專案目錄
cd "$(dirname "$0")"

# 啟動虛擬環境
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ 虛擬環境已啟動"
else
    echo "❌ 找不到 .venv 虛擬環境"
    exit 1
fi

# 檢查依賴
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ 缺少依賴套件"
    echo ""
    echo "請先執行：pip install -r requirements.txt"
    exit 1
fi

echo "✅ 依賴套件正常"
echo ""
echo "啟動中..."
echo ""
echo "=========================================="
echo "  訪問：http://localhost:8000"
echo "  停止：按 Ctrl+C"
echo "=========================================="
echo ""

# 最簡單的啟動方式 - 不使用任何會導致問題的選項
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
