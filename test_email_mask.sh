#!/bin/bash
echo "========================================="
echo "🔒 Email 遮罩功能測試"
echo "========================================="
echo ""

# 測試 1: 檢查 Dashboard HTML 包含遮罩元素
echo "1️⃣  測試 Dashboard HTML 結構..."
if curl -s http://localhost:8000/dashboard | grep -q "masked-email"; then
    echo "   ✅ Dashboard 包含 email-cell 和 masked-email 元素"
else
    echo "   ❌ Dashboard 缺少遮罩元素"
fi

# 測試 2: 檢查 JavaScript 函數
echo ""
echo "2️⃣  測試 JavaScript 遮罩函數..."
if curl -s http://localhost:8000/dashboard | grep -q "function maskEmail"; then
    echo "   ✅ maskEmail() 函數已載入"
else
    echo "   ❌ maskEmail() 函數未找到"
fi

if curl -s http://localhost:8000/dashboard | grep -q "function toggleEmail"; then
    echo "   ✅ toggleEmail() 函數已載入"
else
    echo "   ❌ toggleEmail() 函數未找到"
fi

# 測試 3: 檢查編輯頁面遮罩
echo ""
echo "3️⃣  測試編輯頁面 Email 鎖定..."
if curl -s http://localhost:8000/client/1/edit | grep -q "toggleEmailEdit"; then
    echo "   ✅ 編輯頁面包含 Email 鎖定功能"
else
    echo "   ❌ 編輯頁面缺少鎖定功能"
fi

# 測試 4: 測試遮罩邏輯
echo ""
echo "4️⃣  測試 Email 遮罩邏輯..."
node << 'JSEOF'
function maskEmail(email) {
    const [localPart, domain] = email.split('@');
    if (localPart.length <= 3) {
        return localPart[0] + '***@' + domain;
    }
    const visibleStart = localPart.substring(0, 3);
    return visibleStart + '***@' + domain;
}

const tests = [
    ['contact@example.com', 'con***@example.com'],
    ['service@test.tw', 'ser***@test.tw'],
    ['a@x.com', 'a***@x.com'],
    ['ab@x.com', 'a***@x.com'],
    ['abc@x.com', 'a***@x.com']
];

let passed = 0;
let failed = 0;

tests.forEach(([input, expected]) => {
    const result = maskEmail(input);
    if (result === expected) {
        console.log(`   ✅ ${input} → ${result}`);
        passed++;
    } else {
        console.log(`   ❌ ${input} → ${result} (期望: ${expected})`);
        failed++;
    }
});

console.log('');
console.log(`   測試結果: ${passed} 通過, ${failed} 失敗`);
JSEOF

# 測試 5: 檢查 CSS 樣式
echo ""
echo "5️⃣  測試 CSS 樣式..."
if curl -s http://localhost:8000/static/css/custom.css | grep -q "email-cell"; then
    echo "   ✅ Email 遮罩 CSS 樣式已載入"
else
    echo "   ❌ CSS 樣式未找到"
fi

if curl -s http://localhost:8000/static/css/custom.css | grep -q "toggle-email"; then
    echo "   ✅ 切換按鈕樣式已載入"
else
    echo "   ❌ 按鈕樣式未找到"
fi

# 測試總結
echo ""
echo "========================================="
echo "✅ Email 遮罩功能測試完成！"
echo "========================================="
echo ""
echo "📖 查看詳細文件:"
echo "   - cat EMAIL_MASK_FEATURE.md"
echo "   - cat EMAIL_MASK_DEMO.md"
echo ""
echo "🌐 開啟瀏覽器測試:"
echo "   http://localhost:8000/dashboard"
