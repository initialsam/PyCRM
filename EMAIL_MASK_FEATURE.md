# 📧 Email 遮罩功能說明

## ✨ 新功能

已為 CRM 系統加入 **Email 遮罩保護** 功能，保護客戶隱私資料。

## 🎯 功能特點

### 1. Dashboard 頁面
- **預設隱藏**：Email 自動遮罩顯示
- **可切換顯示**：點擊「顯示」按鈕查看完整 Email
- **逐一控制**：每個客戶的 Email 可獨立顯示/隱藏

### 2. 編輯頁面
- **安全顯示**：編輯客戶時 Email 預設遮罩
- **需要解鎖**：點擊「編輯」按鈕才能修改
- **防誤改**：保護重要聯絡資訊

## 🔐 遮罩規則

### 顯示前 3 個字符 + *** + @域名

| 原始 Email | 遮罩後顯示 |
|-----------|-----------|
| contact@honda-digital.com | con***@honda-digital.com |
| service@green-tech.tw | ser***@green-tech.tw |
| hello@aurora-creative.com | hel***@aurora-creative.com |
| info@star-edu.org | inf***@star-edu.org |
| a@test.com | a***@test.com |
| ab@test.com | a***@test.com |
| abc@test.com | a***@test.com |

### 特殊處理
- Email 長度 ≤ 3 字符：只顯示第 1 個字符
- Email 長度 > 3 字符：顯示前 3 個字符
- **域名始終顯示**：方便識別來源

## 🖱️ 使用方式

### Dashboard 列表
1. 預設所有 Email 都是遮罩狀態
2. 點擊該行的「顯示」按鈕 → 完整顯示 Email
3. 按鈕變為「隱藏」並變綠色
4. 再次點擊「隱藏」→ 恢復遮罩

### 編輯頁面
1. Email 欄位預設為**唯讀**且遮罩顯示
2. 點擊「編輯」按鈕 → 解鎖並顯示完整 Email
3. 按鈕變為紅色「鎖定」
4. 修改完成後點擊「鎖定」→ 重新上鎖

## 📱 視覺設計

### 按鈕狀態
- **顯示按鈕**：灰色背景 (#6c757d)
- **隱藏按鈕**：綠色背景 (#28a745) - 表示 Email 已可見
- **編輯按鈕**：預設樣式
- **鎖定按鈕**：紅色背景 (#ca3c3c) - 提醒處於編輯狀態

### Email 文字
- 使用等寬字體 (Courier New)
- 灰色文字 (#555)
- 遮罩符號使用 ***

## 🔒 安全優勢

1. **預設隱藏**：防止未授權人員看到完整 Email
2. **選擇性顯示**：只在需要時顯示特定客戶的 Email
3. **編輯保護**：防止意外修改重要聯絡資訊
4. **畫面截圖保護**：即使截圖也不會洩露所有 Email

## 💻 技術實作

### 前端實作
- JavaScript 動態遮罩
- 原始資料存於 `data-email` 屬性
- 不影響後端 API 和資料庫
- 純前端處理，無額外網路請求

### 後端不變
- 資料庫儲存完整 Email
- API 回傳完整 Email
- 遮罩僅在瀏覽器顯示層

## 📊 測試驗證

訪問 http://localhost:8000/dashboard 查看效果：

1. ✅ 所有 Email 預設遮罩
2. ✅ 點擊「顯示」可查看完整 Email
3. ✅ 點擊「隱藏」恢復遮罩
4. ✅ 編輯頁面 Email 預設鎖定
5. ✅ 可單獨解鎖編輯

## 🎨 樣式檔案

修改的檔案：
- `app/templates/dashboard.html` - Dashboard 遮罩邏輯
- `app/templates/client_form.html` - 表單編輯保護
- `app/static/css/custom.css` - Email 遮罩樣式

## 🚀 立即體驗

```bash
# 訪問 Dashboard
open http://localhost:8000/dashboard

# 或編輯客戶
open http://localhost:8000/client/1/edit
```

## 📝 注意事項

1. Email 遮罩僅影響前端顯示
2. API 仍回傳完整 Email（供程式使用）
3. 資料庫儲存完整 Email（不受影響）
4. 若需要匯出/列印，可先點擊「顯示全部」

---

**功能已上線並正常運作！** 🎉
