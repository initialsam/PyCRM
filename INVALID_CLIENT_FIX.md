# invalid_client 錯誤解決指南

## 🔴 錯誤說明

`invalid_client` 表示 Google 無法驗證您的 OAuth 客戶端憑證。

## 🎯 最可能的原因

**OAuth 客戶端類型錯誤**

如果您的 OAuth 客戶端是 **"Desktop app"** 類型，會導致此錯誤。
本系統需要 **"Web application"** 類型。

## ✅ 完整解決步驟

### 步驟 1: 檢查現有客戶端類型

1. 前往 [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. 找到您的 OAuth 2.0 客戶端
3. 查看類型是否為 **"Web application"**

### 步驟 2: 建立新的 Web Application 客戶端

如果類型不對，需要建立新的：

1. 點擊「**CREATE CREDENTIALS**」
2. 選擇「**OAuth client ID**」
3. Application type: **Web application**
4. Name: `CRM System` (或任意名稱)

5. **Authorized redirect URIs** 加入以下兩個：
   ```
   http://localhost:8000/auth/callback
   http://localhost:8000/auth/gmail/callback
   ```

6. 點擊「**CREATE**」

7. **重要**：記下或下載 Client ID 和 Client Secret

### 步驟 3: 更新 .env 檔案

編輯 `/mnt/n/vibe/CRM/.env`：

```env
GOOGLE_CLIENT_ID=新的-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=新的-client-secret
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
ALLOWED_EMAILS=helpaction4u@gmail.com
SECRET_KEY=your-secret-key
```

**確認格式**：
- ✅ Client ID 結尾是 `.apps.googleusercontent.com`
- ✅ Client Secret 是一串隨機字元（約 24 字元）

### 步驟 4: 重啟應用

```bash
# 停止當前應用 (Ctrl+C)

# 重新啟動
./RUN_ME.sh
```

### 步驟 5: 測試登入

1. 訪問 http://localhost:8000/login
2. 點擊「使用 Google 帳號登入」
3. 應該成功跳轉到 Google 登入頁面

## 🔍 檢查清單

在重新嘗試前，確認：

- [ ] OAuth 客戶端類型是 **Web application**
- [ ] Redirect URIs 包含 `http://localhost:8000/auth/callback`
- [ ] Client ID 格式正確（.apps.googleusercontent.com）
- [ ] .env 中的 Client ID 和 Secret 已更新
- [ ] 應用已重啟

## 🆘 其他可能原因

### 原因 2: 憑證被停用

檢查：
1. Google Cloud Console
2. Credentials 頁面
3. 確認 OAuth 客戶端狀態是「啟用」

### 原因 3: Client ID 和 Secret 不匹配

確認：
- .env 中的 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET 是從同一個 OAuth 客戶端複製的

### 原因 4: 專案問題

確認：
- Google Cloud Console 中選擇的專案正確
- APIs & Services 中 OAuth consent screen 已設定

## 📞 測試命令

更新後測試：

```bash
# 檢查 .env 設定
cat .env | grep GOOGLE

# 測試應用匯入
source .venv/bin/activate
python -c "import os; print('Client ID:', os.getenv('GOOGLE_CLIENT_ID', 'NOT SET'))"

# 啟動應用
./RUN_ME.sh
```

## ✅ 成功標誌

如果設定正確，點擊登入後應該：
1. 跳轉到 Google 登入頁面
2. 要求您選擇帳號或登入
3. 顯示授權畫面（要求存取您的資料）

---

**最重要**：確認 OAuth 客戶端類型是 **Web application**！
