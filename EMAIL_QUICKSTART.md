# 📧 Email 發送功能 - 快速上手指南

## 🎯 功能簡介

系統已整合 Gmail API，支援批量發送客製化郵件給客戶。包含：
- ✅ 3 種預設模板（請款單、中秋節問候、周年慶優惠）
- ✅ 客戶選擇介面（支援全選/單選）
- ✅ 郵件預覽功能
- ✅ 發送狀態追蹤
- ✅ 發送記錄查詢

## ⚡ 5 分鐘快速設定

### 步驟 1：安裝依賴

```bash
pip install -r requirements.txt
```

### 步驟 2：執行資料庫遷移

```bash
python3 migrate_email_tables.py
```

### 步驟 3：啟動應用並初始化模板

```bash
# 啟動應用
uvicorn app.main:app --reload

# 在另一個終端執行（初始化 3 個預設模板）
curl -X POST http://localhost:8000/api/templates/init
```

### 步驟 4：設定 Gmail API（首次使用）

#### A. 在 Google Cloud Console 設定

1. 前往 https://console.cloud.google.com/
2. 啟用 **Gmail API**
3. 建立 **OAuth 2.0 憑證**（類型：Desktop app）
4. 下載 JSON 檔案 → 重新命名為 `credentials.json`
5. 放到專案根目錄

#### B. 首次認證

1. Dashboard → 點擊「📧 發送郵件」
2. 選擇模板和客戶
3. 點擊「發送郵件」
4. **瀏覽器會自動開啟**進行 Google 認證
5. 允許應用存取 Gmail 發送權限
6. ✅ 完成！`token.pickle` 會自動建立

## 📖 使用方式

### 發送郵件

1. **登入系統** → Dashboard
2. **點擊「📧 發送郵件」**
3. **選擇郵件模板**：
   - 💰 請款單
   - 🌕 中秋節問候
   - 🎉 周年慶優惠
4. **選擇收件客戶**（可全選）
5. **（選填）預覽郵件**
6. **點擊「📤 發送郵件」**
7. ✅ 查看發送結果

### 查看發送記錄

Dashboard → 點擊「📬 發送記錄」

- 查看所有郵件發送歷史
- 成功 ✅ / 失敗 ❌ 狀態
- 錯誤訊息（如果失敗）

## 🎨 郵件模板

### 變數替換

所有模板都支援以下變數：

```html
{{client_name}}    → 客戶名稱
{{project_name}}   → 專案名稱
{{project_cost}}   → 專案費用（自動格式化）
```

**範例：**

模板內容：
```html
<p>親愛的 <strong>{{client_name}}</strong> 您好，</p>
<p>專案：{{project_name}}，費用：{{project_cost}}</p>
```

實際發送：
```html
<p>親愛的 <strong>王小明</strong> 您好，</p>
<p>專案：官網重新設計，費用：NT$ 50,000</p>
```

## 📊 3 種預設模板

### 1. 💰 請款單（invoice）

- **主旨**：【請款通知】{{project_name}} 專案款項
- **用途**：請款通知
- **風格**：綠色主題、專業格式
- **內容**：包含客戶名稱、專案名稱、費用

### 2. 🌕 中秋節問候（greeting）

- **主旨**：🌕 中秋佳節愉快！
- **用途**：節日問候
- **風格**：溫馨漸變色、節日氛圍
- **內容**：節日祝福、感謝語

### 3. 🎉 周年慶優惠（promotion）

- **主旨**：🎉 周年慶特惠活動 - 限時優惠！
- **用途**：促銷活動
- **風格**：紫色主題、優惠資訊突出
- **內容**：優惠方案、活動期間

## ⚠️ 注意事項

### Gmail API 限制

- **免費帳號**：約 500 封/天
- **Google Workspace**：約 2000 封/天
- 建議發送速率：每秒不超過 1 封

### 安全性

- ✅ `credentials.json` 和 `token.pickle` 已加入 `.gitignore`
- ⚠️ 不要將認證檔案上傳到 Git 或公開分享

### 故障排除

#### ❌ 找不到 credentials.json
→ 確認檔案在專案根目錄且名稱正確

#### ❌ 認證失敗
→ 刪除 `token.pickle` 並重新認證

#### ❌ 發送失敗
→ 檢查 Email 格式、API 配額、查看錯誤記錄

## 📁 相關檔案

```
CRM/
├── app/
│   ├── email_service.py          # Gmail API 服務
│   ├── routers/emails.py         # 郵件路由
│   ├── templates/
│   │   ├── send_email.html       # 發送頁面
│   │   └── email_logs.html       # 記錄頁面
│   └── models.py                 # EmailTemplate, EmailLog
├── credentials.json              # Gmail API 憑證（需自行設定）
├── token.pickle                  # OAuth Token（自動生成）
├── migrate_email_tables.py       # 資料庫遷移
├── setup_email.sh                # 快速設定腳本
├── test_email_setup.sh           # 測試檢查腳本
└── EMAIL_SEND_GUIDE.md           # 完整說明文件
```

## 🚀 一鍵檢查

```bash
# 執行完整檢查
./test_email_setup.sh

# 快速設定
./setup_email.sh
```

## 📞 更多資訊

詳細說明請參考：
- [完整設定指南](EMAIL_SEND_GUIDE.md)
- [Gmail API 文件](https://developers.google.com/gmail/api)
- [OAuth 2.0 設定](https://developers.google.com/identity/protocols/oauth2)

---

**🎉 完成設定後，立即開始發送客製化郵件給您的客戶！**
