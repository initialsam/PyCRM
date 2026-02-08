# Google 登入功能 - 快速啟動指南

## 🎯 快速開始（5 分鐘設定）

### 步驟 1: 取得 Google OAuth 憑證

1. 前往 https://console.cloud.google.com/
2. 建立或選擇專案
3. 「API 和服務」→「憑證」→「建立憑證」→「OAuth 用戶端 ID」
4. 應用程式類型：**網頁應用程式**
5. 已授權的重新導向 URI：
   - 本機：`http://localhost:8000/auth/callback`
   - 正式：`https://your-domain.com/auth/callback`
6. 複製 **Client ID** 和 **Client Secret**

### 步驟 2: 設定環境變數

建立或編輯 `.env` 檔案：

```bash
# 資料庫
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crm_db

# Google OAuth（貼上你的憑證）
GOOGLE_CLIENT_ID=你的-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=你的-client-secret

# Session 密鑰（執行下面的命令生成）
SECRET_KEY=請執行-openssl-rand-hex-32-生成
```

生成 SECRET_KEY：
```bash
openssl rand -hex 32
```

### 步驟 3: 啟動應用

```bash
# 安裝依賴（自動）
uv run uvicorn app.main:app --reload

# 或使用 start.sh
./start.sh
```

### 步驟 4: 測試登入

1. 開啟瀏覽器：http://localhost:8000
2. 會自動導向登入頁面
3. 點擊「使用 Google 帳號登入」
4. 選擇 Google 帳號並授權
5. 成功登入後會看到 Dashboard

## ✅ 驗證設定

執行驗證腳本檢查所有設定：
```bash
./verify_google_login.sh
```

## 🔒 安全性提醒

- ✅ **SECRET_KEY**: 請務必使用隨機生成的長密鑰
- ✅ **HTTPS**: 生產環境必須使用 HTTPS
- ✅ **憑證保密**: 不要將 Client Secret 提交到 Git
- ✅ **重定向 URI**: 確保完全符合 Google Console 設定

## 📖 詳細文件

- [GOOGLE_LOGIN_SETUP.md](GOOGLE_LOGIN_SETUP.md) - 完整設定指南
- [GOOGLE_LOGIN_IMPLEMENTATION.md](GOOGLE_LOGIN_IMPLEMENTATION.md) - 技術實作說明

## 🐛 常見問題

### Q: 出現 "redirect_uri_mismatch" 錯誤？
**A**: 檢查 Google Console 的重新導向 URI 是否完全符合（包含 http/https）

### Q: 登入後一直要求重新登入？
**A**: 檢查 SECRET_KEY 是否已設定，重啟應用會清除 Session

### Q: 無法顯示登入按鈕？
**A**: 檢查 templates/login.html 是否存在，確認路由設定正確

### Q: API 回傳 401 錯誤？
**A**: 未登入無法使用 API，請先透過瀏覽器登入

## 📦 Zeabur 部署

在 Zeabur Dashboard 設定環境變數：
- `DATABASE_URL` (PostgreSQL Service 自動提供)
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `SECRET_KEY`

重新導向 URI 使用：`https://your-app.zeabur.app/auth/callback`

## 🎉 完成！

設定完成後，你的 CRM 系統已經：
- ✅ 需要 Google 登入才能訪問
- ✅ 所有頁面和 API 都受保護
- ✅ 顯示使用者資訊
- ✅ 提供登出功能

享受安全的 CRM 系統！🚀
