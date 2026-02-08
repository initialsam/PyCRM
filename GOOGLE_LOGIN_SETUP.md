# Google OAuth 登入設定指南

## 功能說明
本系統已整合 Google OAuth 2.0 登入功能，只允許使用 Google 帳號登入存取 CRM 系統。

## 設定步驟

### 1. 建立 Google OAuth 憑證

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google+ API：
   - 在左側選單選擇「API 和服務」>「程式庫」
   - 搜尋 "Google+ API" 並啟用

4. 建立 OAuth 2.0 憑證：
   - 選擇「API 和服務」>「憑證」
   - 點擊「建立憑證」>「OAuth 用戶端 ID」
   - 應用程式類型選擇「網頁應用程式」
   - 名稱：CRM System（或自訂名稱）
   - 已授權的重新導向 URI：
     - 本機測試：`http://localhost:8000/auth/callback`
     - 正式環境：`https://your-domain.com/auth/callback`
   
5. 建立後會得到：
   - Client ID（客戶端 ID）
   - Client Secret（客戶端密鑰）

### 2. 設定環境變數

#### 本機開發
在專案根目錄建立 `.env` 檔案：

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/crm_db
GOOGLE_CLIENT_ID=你的-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=你的-client-secret
SECRET_KEY=使用-openssl-rand-hex-32-生成的隨機密鑰
```

生成 SECRET_KEY：
```bash
openssl rand -hex 32
```

#### Zeabur 部署
在 Zeabur Dashboard 的環境變數設定中新增：
- `GOOGLE_CLIENT_ID`: 你的 Google Client ID
- `GOOGLE_CLIENT_SECRET`: 你的 Google Client Secret
- `SECRET_KEY`: 隨機生成的密鑰

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 啟動應用程式

```bash
uvicorn app.main:app --reload
```

## 使用說明

1. 訪問系統會自動導向登入頁面 `/login`
2. 點擊「使用 Google 帳號登入」按鈕
3. 選擇或登入 Google 帳號
4. 授權後會自動導向 Dashboard

## 受保護的路由

以下路由都需要登入才能存取：
- `/` - 首頁（導向 Dashboard）
- `/dashboard` - 控制台
- `/client/new` - 新增客戶
- `/client/{id}/edit` - 編輯客戶
- `/import` - 匯入 CSV

## 登出
點擊右上角的「登出」按鈕即可登出系統。

## 安全性說明

- Session 使用加密儲存
- OAuth token 僅用於認證，不儲存密碼
- 請務必在生產環境使用強隨機 SECRET_KEY
- HTTPS 環境下 Session 更安全

## 疑難排解

### 錯誤：redirect_uri_mismatch
- 檢查 Google Console 中的授權重新導向 URI 是否正確
- 確保網址包含完整的 protocol (http:// 或 https://)

### 無法登入
- 確認環境變數設定正確
- 檢查 Google OAuth 憑證是否有效
- 查看應用程式日誌了解詳細錯誤資訊

### Session 失效
- 檢查 SECRET_KEY 是否設定
- 重新啟動應用程式後 Session 會失效，需重新登入
