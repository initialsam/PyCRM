#!/bin/bash
echo "=== CRM 系統測試腳本 ==="
echo ""

# 測試統計 API
echo "1. 測試統計 API:"
curl -s http://localhost:8000/api/clients/statistics | jq
echo ""

# 測試客戶列表
echo "2. 測試客戶列表 (前 3 筆):"
curl -s http://localhost:8000/api/clients/ | jq '.[0:3] | .[] | {id, client_name, project_name, project_cost}'
echo ""

# 測試搜尋功能
echo "3. 測試搜尋功能 (搜尋'智能'):"
curl -s "http://localhost:8000/api/clients/?search=智能" | jq '.[] | {client_name, project_name}'
echo ""

# 測試 Dashboard
echo "4. 測試 Dashboard 頁面:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/dashboard
echo ""

echo "✅ 所有測試完成！"
echo "🌐 請在瀏覽器開啟: http://localhost:8000"
