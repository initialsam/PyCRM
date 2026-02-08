#!/bin/bash
echo "========================================="
echo "🔧 Email 遮罩功能修復測試"
echo "========================================="
echo ""

echo "1️⃣  檢查資料庫中的 Email 格式"
echo ""
echo "前 3 筆客戶的 Email："
curl -s http://localhost:8000/api/clients/ | jq -r '.[0:3] | .[] | "\(.id). \(.client_name): \(.email)"'

echo ""
echo "2️⃣  檢查是否有遮罩格式存在資料庫"
MASKED_COUNT=$(curl -s http://localhost:8000/api/clients/ | jq -r '.[] | .email' | grep -c '\*\*\*')
if [ "$MASKED_COUNT" -eq 0 ]; then
    echo "   ✅ 資料庫中沒有遮罩格式的 Email"
else
    echo "   ❌ 資料庫中有 $MASKED_COUNT 筆遮罩格式的 Email"
    echo "   需要修復的記錄："
    curl -s http://localhost:8000/api/clients/ | jq -r '.[] | select(.email | contains("***")) | "\(.id). \(.client_name): \(.email)"'
fi

echo ""
echo "3️⃣  測試編輯表單的 originalEmail 變數"
ORIGINAL_EMAIL=$(curl -s http://localhost:8000/client/1/edit | grep -o "originalEmail = '[^']*'" | head -1)
echo "   $ORIGINAL_EMAIL"
if echo "$ORIGINAL_EMAIL" | grep -q '\*\*\*'; then
    echo "   ❌ originalEmail 包含遮罩符號"
else
    echo "   ✅ originalEmail 是完整的 Email"
fi

echo ""
echo "4️⃣  測試 Dashboard 的 data-email 屬性"
DATA_EMAIL=$(curl -s http://localhost:8000/dashboard | grep -o 'data-email="[^"]*"' | head -1)
echo "   $DATA_EMAIL"
if echo "$DATA_EMAIL" | grep -q '\*\*\*'; then
    echo "   ❌ data-email 包含遮罩符號"
else
    echo "   ✅ data-email 是完整的 Email"
fi

echo ""
echo "5️⃣  測試編輯客戶但不修改 Email"
echo "   更新客戶 1 的名稱..."
RESULT=$(curl -s -X PUT http://localhost:8000/api/clients/1 \
  -H "Content-Type: application/json" \
  -d '{"client_name": "宏達數位科技"}')

UPDATED_EMAIL=$(echo $RESULT | jq -r '.email')
echo "   更新後的 Email: $UPDATED_EMAIL"

if echo "$UPDATED_EMAIL" | grep -q '\*\*\*'; then
    echo "   ❌ Email 被錯誤地保存為遮罩格式"
else
    echo "   ✅ Email 保持完整格式"
fi

echo ""
echo "========================================="
echo "✅ Email 遮罩功能測試完成"
echo "========================================="
echo ""
echo "修復內容："
echo "  1. 表單提交時使用原始 Email（不提交遮罩值）"
echo "  2. originalEmail 變數正確保存完整 Email"
echo "  3. Dashboard 的 data-email 包含完整 Email"
echo "  4. 遮罩僅在前端顯示，不影響資料庫"
echo ""
echo "🌐 訪問 Dashboard 測試："
echo "   http://localhost:8000/dashboard"
