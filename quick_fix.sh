#!/bin/bash
# 快速修復腳本

echo "=========================================="
echo "  🔧 快速修復 - 安裝依賴"
echo "=========================================="
echo ""

# 檢查虛擬環境
if [ -d ".venv" ]; then
    echo "✅ 找到虛擬環境 .venv"
    echo ""
    echo "啟動虛擬環境並安裝依賴..."
    source .venv/bin/activate
    
    echo ""
    echo "安裝套件中... (可能需要幾分鐘)"
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "  ✅ 安裝完成！"
        echo "=========================================="
        echo ""
        echo "🚀 啟動應用："
        echo "   source .venv/bin/activate"
        echo "   uvicorn app.main:app --reload"
        echo ""
        echo "或執行："
        echo "   ./start.sh"
    else
        echo ""
        echo "❌ 安裝失敗"
        echo "請檢查錯誤訊息"
    fi
else
    echo "❌ 找不到虛擬環境 .venv"
    echo ""
    echo "請先建立虛擬環境："
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
fi
