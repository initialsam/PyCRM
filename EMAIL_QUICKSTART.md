# ⚡ 快速初始化郵件模板

## 最簡單的方法（30秒完成）

### 步驟 1: 登入系統
訪問 `https://pycrm.zeabur.app/login` 並登入

### 步驟 2: 開啟開發者工具
按 **F12** 鍵（或右鍵 → 檢查）

### 步驟 3: 切換到 Console 標籤
點擊 **Console** 標籤

### 步驟 4: 貼上並執行
複製下面的代碼，貼到 Console 中，按 **Enter**：

```javascript
fetch('/api/templates/init', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
})
.then(response => response.json())
.then(data => {
    console.log('✓ 完成:', data);
    alert('✅ 郵件模板已建立！\n\n包含：\n1. 請款單\n2. 中秋節問候\n3. 周年慶優惠\n\n請重新整理頁面。');
})
.catch(error => {
    console.error('錯誤:', error);
    alert('❌ 初始化失敗，請檢查 Console');
});
```

### 步驟 5: 重新整理頁面
按 **F5** 或點擊重新整理按鈕

### 步驟 6: 確認模板
前往 `/send-email`，應該看到三個模板選項：
- 📄 請款單
- 🌕 中秋節問候  
- 🎉 周年慶優惠

---

## 完成！

現在可以：
1. 選擇模板
2. 選擇客戶
3. 發送郵件

模板會自動填入客戶姓名、專案名稱和金額。

---

**詳細說明請參閱：`EMAIL_TEMPLATE_SETUP.md`**
