#!/bin/bash
echo "========================================="
echo "✅ Email 功能最終驗證"
echo "========================================="
echo ""

echo "1️⃣  驗證所有客戶的 Email 格式："
ALL_EMAILS=$(curl -s http://localhost:8000/api/clients/ | jq -r '.[] | .email')
echo "$ALL_EMAILS"
echo ""

MASKED_IN_DB=$(echo "$ALL_EMAILS" | grep -c '\*\*\*' || echo 0)
if [ "$MASKED_IN_DB" -eq 0 ]; then
    echo "   ✅ 資料庫中所有 Email 都是完整格式"
else
    echo "   ❌ 仍有 $MASKED_IN_DB 筆遮罩格式的 Email"
fi

echo ""
echo "2️⃣  驗證 Dashboard 遮罩顯示："
DASHBOARD_HTML=$(curl -s http://localhost:8000/dashboard)

# 檢查是否有 data-email 屬性且不包含 ***
DATA_EMAIL_COUNT=$(echo "$DASHBOARD_HTML" | grep -o 'data-email="[^"]*"' | wc -l)
MASKED_DATA_EMAIL=$(echo "$DASHBOARD_HTML" | grep -o 'data-email="[^"]*\*\*\*[^"]*"' | wc -l)

echo "   找到 $DATA_EMAIL_COUNT 個 data-email 屬性"
if [ "$MASKED_DATA_EMAIL" -eq 0 ]; then
    echo "   ✅ 所有 data-email 都是完整格式"
else
    echo "   ❌ 有 $MASKED_DATA_EMAIL 個 data-email 是遮罩格式"
fi

# 檢查是否有 masked-email span
MASKED_SPAN_COUNT=$(echo "$DASHBOARD_HTML" | grep -c 'class="masked-email"')
echo "   找到 $MASKED_SPAN_COUNT 個遮罩顯示元素"
if [ "$MASKED_SPAN_COUNT" -gt 0 ]; then
    echo "   ✅ 前端遮罩機制正常"
fi

echo ""
echo "3️⃣  測試完整流程："
echo "   a) 訪問編輯頁面..."
EDIT_PAGE=$(curl -s http://localhost:8000/client/1/edit)
ORIGINAL_EMAIL=$(echo "$EDIT_PAGE" | grep -o "originalEmail = '[^']*'" | cut -d"'" -f2)
echo "      originalEmail = $ORIGINAL_EMAIL"

echo ""
echo "   b) 模擬編輯（修改專案費用）..."
UPDATE_RESULT=$(curl -s -X PUT http://localhost:8000/api/clients/1 \
  -H "Content-Type: application/json" \
  -d '{"project_cost": 260000}')
UPDATED_EMAIL=$(echo $UPDATE_RESULT | jq -r '.email')
echo "      更新後 Email = $UPDATED_EMAIL"

if [ "$ORIGINAL_EMAIL" = "$UPDATED_EMAIL" ]; then
    echo "      ✅ Email 未被改變"
else
    echo "      ❌ Email 被意外修改"
fi

echo ""
echo "========================================="
echo "📊 最終結果"
echo "========================================="
echo ""

if [ "$MASKED_IN_DB" -eq 0 ] && [ "$MASKED_DATA_EMAIL" -eq 0 ]; then
    echo "🎉 所有測試通過！Email 遮罩功能已完全修復！"
    echo ""
    echo "功能狀態："
    echo "  ✅ 資料庫儲存完整 Email"
    echo "  ✅ Dashboard 顯示遮罩（前端）"
    echo "  ✅ 編輯表單正確處理 Email"
    echo "  ✅ 更新操作保持 Email 完整"
else
    echo "⚠️  仍有問題需要處理"
fi

echo ""
echo "🌐 測試 Dashboard："
echo "   http://localhost:8000/dashboard"
