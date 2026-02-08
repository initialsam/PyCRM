#!/bin/bash
# CRM 系統啟動腳本

echo "🚀 正在啟動 CRM 專案管理系統..."
echo ""

# 檢查 PostgreSQL
if ! systemctl is-active --quiet postgresql; then
    echo "⚠️  PostgreSQL 未運行，正在啟動..."
    sudo systemctl start postgresql
fi

# 檢查資料庫
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw crm_db; then
    echo "📦 建立資料庫 crm_db..."
    sudo -u postgres psql -c "CREATE DATABASE crm_db;"
fi

# 啟動應用
cd /mnt/n/vibe/CRM
echo "🔧 啟動 FastAPI 伺服器..."
nohup uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/fastapi-server.log 2>&1 &

sleep 5

# 檢查是否成功啟動
if curl -s http://localhost:8000/api/clients/statistics > /dev/null; then
    echo ""
    echo "✅ CRM 系統已成功啟動！"
    echo ""
    echo "📊 Dashboard: http://localhost:8000"
    echo "📖 API 文件: http://localhost:8000/docs"
    echo "📋 查看日誌: tail -f /tmp/fastapi-server.log"
    echo ""
else
    echo "❌ 啟動失敗，請檢查日誌: tail -f /tmp/fastapi-server.log"
fi
