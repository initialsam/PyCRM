# Google OAuth Redirect URI 設定指南

## 問題
錯誤：`redirect_uri_mismatch` - 重新導向 URI 不匹配

## 解決方案

### 1. 前往 Google Cloud Console

訪問：https://console.cloud.google.com/apis/credentials

### 2. 選擇你的 OAuth 2.0 客戶端 ID

找到你正在使用的 OAuth 客戶端 ID 並點擊編輯。

### 3. 新增授權的重新導向 URI

在「已授權的重新導向 URI」區段，新增以下兩個 URI：

```
https://pycrm.zeabur.app/auth/callback
https://pycrm.zeabur.app/auth/gmail/callback
```

⚠️ **重要提示**：
- 必須使用 `https://`（不是 `http://`）
- URI 必須完全一致，包括結尾沒有 `/`
- 如果你的域名不同，請替換 `pycrm.zeabur.app` 為你的實際域名

### 4. 儲存設定

點擊「儲存」按鈕。

### 5. 設定環境變數（可選但推薦）

在 Zeabur 環境變數中設定：

```bash
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

這樣可以確保 redirect URI 始終使用正確的值。

## 完整的 Google Cloud Console 設定檢查清單

### OAuth 同意畫面
- [ ] 設定應用程式名稱
- [ ] 設定使用者支援電子郵件
- [ ] 設定開發人員聯絡資訊

### OAuth 範圍（Scopes）
- [ ] `openid`
- [ ] `.../auth/userinfo.email`
- [ ] `.../auth/userinfo.profile`
- [ ] `.../auth/gmail.send`

### 已授權的重新導向 URI
- [ ] `https://pycrm.zeabur.app/auth/callback`
- [ ] `https://pycrm.zeabur.app/auth/gmail/callback`

### 測試使用者（如果未發布）
- [ ] 新增你的 Gmail 地址作為測試使用者

## 驗證設定

完成設定後：

1. 清除瀏覽器 cookies
2. 訪問 `https://pycrm.zeabur.app/login`
3. 點擊 Google 登入
4. 應該能成功登入
5. 訪問 `/send-email`
6. 點擊「授權 Gmail API」
7. 應該能成功授權

## 常見問題

**Q: 我已經添加了 URI，但還是顯示錯誤？**
A: 
1. 確認 URI 完全一致（包括 https 和結尾）
2. 等待 5-10 分鐘讓 Google 更新設定
3. 清除瀏覽器 cookies 後重試

**Q: 我應該使用 http 還是 https？**
A: 在 Zeabur 部署時必須使用 `https://`。本地開發時使用 `http://localhost:8000`。

**Q: 我需要設定哪些環境變數？**
A: 必需的：
```bash
GOOGLE_CLIENT_ID=你的client_id
GOOGLE_CLIENT_SECRET=你的client_secret
SECRET_KEY=隨機長字串
ALLOWED_EMAILS=允許登入的email列表
```

可選但推薦：
```bash
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

## 快速修復步驟

1. ✅ 前往 https://console.cloud.google.com/apis/credentials
2. ✅ 選擇 OAuth 2.0 客戶端 ID
3. ✅ 新增重新導向 URI：
   - `https://pycrm.zeabur.app/auth/callback`
   - `https://pycrm.zeabur.app/auth/gmail/callback`
4. ✅ 儲存
5. ✅ 等待 5 分鐘
6. ✅ 清除瀏覽器 cookies
7. ✅ 重新測試登入

## 截圖位置（應該看起來像這樣）

```
OAuth 2.0 客戶端 ID
├── 名稱：[你的應用程式名稱]
├── 客戶端 ID：[your-client-id].apps.googleusercontent.com
├── 客戶端密鑰：[your-client-secret]
└── 已授權的重新導向 URI：
    ├── https://pycrm.zeabur.app/auth/callback
    └── https://pycrm.zeabur.app/auth/gmail/callback
```

## 程式碼已修正

我已經更新了 `app/main.py`，當檢測到從 `zeabur.app` 訪問時，會自動使用 `https://`：

```python
if 'zeabur.app' in str(request.base_url):
    redirect_uri = redirect_uri.replace('http://', 'https://')
```

這確保了即使在 proxy 後面，redirect URI 也會使用正確的 scheme。
