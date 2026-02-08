# Gmail API 郵件發送功能說明

## 📧 功能概述

完整的郵件發送系統，支援：
- ✅ 使用 Gmail API 發送郵件
- ✅ 3 種預設郵件模板（請款單、中秋節問候、周年慶優惠）
- ✅ 批量選擇客戶發送
- ✅ 郵件預覽功能
- ✅ 發送狀態追蹤
- ✅ 發送記錄查詢

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定 Gmail API

#### 步驟 A：建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Gmail API：
   - 左側選單 → APIs & Services → Library
   - 搜尋 "Gmail API"
   - 點擊 "Enable"

#### 步驟 B：建立 OAuth 2.0 憑證

1. APIs & Services → Credentials
2. 點擊 "Create Credentials" → "OAuth client ID"
3. 應用程式類型選擇：**Desktop app**
4. 名稱：隨意命名（例如：CRM Email Sender）
5. 點擊 "Create"
6. 下載 JSON 檔案
7. 將檔案重新命名為 `credentials.json`
8. 放到專案根目錄 `/mnt/n/vibe/CRM/credentials.json`

#### 步驟 C：設定 OAuth 同意畫面

1. APIs & Services → OAuth consent screen
2. User Type 選擇 "External"（外部）
3. 填寫應用程式資訊
4. Scopes 加入：`https://www.googleapis.com/auth/gmail.send`
5. 測試使用者加入你的 Gmail 帳號

### 3. 初始化資料庫和模板

```bash
# 啟動應用
uvicorn app.main:app --reload

# 開啟瀏覽器登入系統後，執行：
curl -X POST http://localhost:8000/api/templates/init
```

### 4. 首次認證

第一次使用時：
1. 前往 Dashboard → 📧 發送郵件
2. 選擇模板和客戶後點擊發送
3. 系統會自動開啟瀏覽器進行 Google 認證
4. 允許應用存取 Gmail 發送權限
5. 認證完成後，`token.pickle` 會自動建立並儲存憑證

## 📝 使用方式

### 發送郵件流程

1. **登入系統** → Dashboard
2. **點擊「📧 發送郵件」**
3. **選擇郵件模板**：
   - 💰 請款單
   - 🌕 中秋節問候
   - 🎉 周年慶優惠
4. **選擇收件客戶**：
   - 可單選或全選
   - 顯示客戶名稱、Email、專案名稱
5. **預覽郵件**（選填）：
   - 查看郵件內容和變數替換效果
6. **發送郵件**：
   - 確認後點擊「📤 發送郵件」
   - 系統會顯示發送進度和結果

### 查看發送記錄

1. Dashboard → 📬 發送記錄
2. 查看所有郵件發送歷史
3. 包含狀態：成功 ✅ / 失敗 ❌
4. 如果失敗會顯示錯誤訊息

## 📧 郵件模板變數

所有模板都支援以下變數替換：

- `{{client_name}}` - 客戶名稱
- `{{project_name}}` - 專案名稱
- `{{project_cost}}` - 專案費用（自動格式化為 NT$ X,XXX）

範例：
```html
<p>親愛的 <strong>{{client_name}}</strong> 您好，</p>
<p>關於 <strong>{{project_name}}</strong> 專案，費用為 {{project_cost}}</p>
```

實際發送時會替換為：
```html
<p>親愛的 <strong>王小明</strong> 您好，</p>
<p>關於 <strong>官網重新設計</strong> 專案，費用為 NT$ 50,000</p>
```

## 🗂 資料庫結構

### EmailTemplate（郵件模板）

```python
id: int                    # 模板 ID
name: str                  # 模板名稱
subject: str               # 郵件主旨
content: str               # 郵件內容（HTML）
template_type: str         # 類型：invoice, greeting, promotion
is_active: bool            # 是否啟用
created_at: datetime       # 建立時間
updated_at: datetime       # 更新時間
```

### EmailLog（發送記錄）

```python
id: int                    # 記錄 ID
client_id: int             # 客戶 ID
client_email: str          # 收件 Email
template_id: int           # 使用的模板 ID
subject: str               # 郵件主旨
status: str                # 狀態：pending, sent, failed
error_message: str         # 錯誤訊息（如果失敗）
sent_at: datetime          # 發送時間
created_at: datetime       # 建立時間
```

## 🔧 API 端點

### 初始化模板
```http
POST /api/templates/init
```
建立預設的 3 個郵件模板

### 取得模板列表
```http
GET /api/templates
```
返回所有啟用的郵件模板

### 發送郵件
```http
POST /api/emails/send
Content-Type: application/json

{
  "template_id": 1,
  "client_ids": [1, 2, 3]
}
```

## 🎨 預設模板

### 1. 💰 請款單 (invoice)
- 主旨：【請款通知】{{project_name}} 專案款項
- 用途：請款通知
- 特色：綠色主題、專業格式

### 2. 🌕 中秋節問候 (greeting)
- 主旨：🌕 中秋佳節愉快！
- 用途：節日問候
- 特色：溫馨漸變色、節日氛圍

### 3. 🎉 周年慶優惠 (promotion)
- 主旨：🎉 周年慶特惠活動 - 限時優惠！
- 用途：促銷活動
- 特色：紫色主題、優惠資訊突出

## ⚠️ 注意事項

### Gmail API 限制

1. **每日發送限制**：
   - 免費帳號：約 500 封/天
   - Google Workspace：約 2000 封/天

2. **發送速率限制**：
   - 建議每秒不超過 1 封
   - 批量發送建議加入延遲

3. **收件人限制**：
   - 每封郵件最多 100 個收件人

### 安全性

- ✅ `credentials.json` 已加入 `.gitignore`
- ✅ `token.pickle` 已加入 `.gitignore`
- ✅ 不要將認證檔案上傳到 Git
- ✅ Zeabur 部署需要手動上傳認證檔案

### 故障排除

#### 問題：找不到 credentials.json
**解決**：確認檔案在專案根目錄且名稱正確

#### 問題：認證失敗
**解決**：
1. 刪除 `token.pickle`
2. 重新執行發送郵件
3. 重新進行 OAuth 認證

#### 問題：發送失敗
**解決**：
1. 檢查收件人 Email 格式
2. 確認 Gmail API 配額未超限
3. 查看 EmailLog 的 error_message

## 📦 檔案結構

```
CRM/
├── app/
│   ├── email_service.py          # Gmail API 服務
│   ├── models.py                 # 資料模型（新增 EmailTemplate, EmailLog）
│   ├── schemas.py                # Pydantic Schema
│   ├── routers/
│   │   └── emails.py             # 郵件路由
│   └── templates/
│       ├── send_email.html       # 發送郵件頁面
│       └── email_logs.html       # 發送記錄頁面
├── credentials.json              # Gmail API 憑證（需自行下載）
├── token.pickle                  # OAuth Token（自動生成）
└── EMAIL_SEND_GUIDE.md           # 本文件
```

## 🎯 未來擴展

可考慮新增：
- [ ] 自訂郵件模板管理介面
- [ ] 排程發送功能
- [ ] 附件上傳功能
- [ ] 發送統計圖表
- [ ] Email 開信率追蹤
- [ ] 取消訂閱功能
- [ ] A/B 測試功能

## 📞 支援

如有問題請聯繫系統管理員或查看：
- [Gmail API 文件](https://developers.google.com/gmail/api)
- [OAuth 2.0 設定指南](https://developers.google.com/identity/protocols/oauth2)
