#!/bin/bash
echo "========================================="
echo "📅 客戶排序功能測試"
echo "========================================="
echo ""

echo "1️⃣  當前客戶排序（前 5 筆）："
curl -s http://localhost:8000/api/clients/ | jq -r '.[] | "\(.id) | \(.client_name) | 更新: \(.updated_at // "未更新") | 建立: \(.created_at)"' | head -5
echo ""

echo "2️⃣  更新 ID 3 的客戶..."
curl -s -X PUT http://localhost:8000/api/clients/3 \
  -H "Content-Type: application/json" \
  -d '{"project_cost": 100000}' > /dev/null
echo "   ✅ 已更新"
sleep 1

echo ""
echo "3️⃣  更新後的排序（ID 3 應該排第一）："
curl -s http://localhost:8000/api/clients/ | jq -r '.[] | "\(.id) | \(.client_name) | 更新: \(.updated_at // "未更新")"' | head -5
echo ""

echo "4️⃣  驗證排序邏輯："
FIRST_ID=$(curl -s http://localhost:8000/api/clients/ | jq -r '.[0].id')
if [ "$FIRST_ID" = "3" ]; then
    echo "   ✅ 排序正確：最新修改的客戶排在第一位"
else
    echo "   ❌ 排序錯誤：第一位應該是 ID 3，實際是 ID $FIRST_ID"
fi

echo ""
echo "5️⃣  檢查 Dashboard HTML："
if curl -s http://localhost:8000/dashboard | grep -q "排序：最後修改時間"; then
    echo "   ✅ Dashboard 顯示排序說明"
else
    echo "   ❌ Dashboard 缺少排序說明"
fi

if curl -s http://localhost:8000/dashboard | grep -q "updated-badge"; then
    echo "   ✅ Dashboard 顯示更新標記"
else
    echo "   ❌ Dashboard 缺少更新標記"
fi

echo ""
echo "========================================="
echo "✅ 排序功能測試完成！"
echo "========================================="
echo ""
echo "排序規則："
echo "  1. 有 updated_at 的記錄優先（新→舊）"
echo "  2. 沒有 updated_at 的記錄按 created_at（新→舊）"
echo ""
echo "🌐 訪問 Dashboard 查看："
echo "   http://localhost:8000/dashboard"
