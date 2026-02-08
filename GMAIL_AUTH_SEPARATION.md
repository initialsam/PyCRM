# Gmail API 授權分離說明

## 問題
之前 Gmail API 授權和登入授權使用相同的 OAuth 配置，導致授權衝突和失敗。

## 解決方案

### 1. 分離兩個 OAuth 配置

在 `app/auth.py` 中註冊了兩個不同的 OAuth 客戶端：

```python
# 登入用的 OAuth (基本權限)
oauth.register(
    name='google',
    scope='openid email profile'
)

# Gmail API 用的 OAuth (包含 gmail.send 權限)
oauth.register(
    name='google_gmail',
    scope='openid email profile https://www.googleapis.com/auth/gmail.send'
)
```

### 2. 新的授權流程

#### 登入流程
- URL: `/auth/login` → `/auth/callback`
- 使用: `oauth.google`
- 權限: `openid email profile`
- Session: `user` (儲存用戶資訊)

#### Gmail API 授權流程
- URL: `/auth/gmail/login` → `/auth/gmail/callback`
- 使用: `oauth.google_gmail`
- 權限: `openid email profile gmail.send`
- Session: `gmail_token` (儲存 Gmail API token)

### 3. Token 管理

**登入 Token**
- 儲存在 `request.session['user']`
- 包含用戶基本資訊 (email, name, picture)
- 用於身份驗證和頁面訪問控制

**Gmail Token**
- 儲存在 `request.session['gmail_token']`
- 包含 access_token, refresh_token
- 用於發送郵件時的 Gmail API 授權

### 4. 發送郵件流程

1. 用戶登入系統 (使用 `/auth/login`)
2. 前往 `/send-email` 頁面
3. 檢查是否有 Gmail 授權
   - 如果沒有，顯示"授權 Gmail API"按鈕
   - 點擊後導向 `/auth/gmail/login`
4. 完成 Gmail 授權後返回 `/send-email`
5. 發送郵件時使用 session 中的 `gmail_token`

### 5. 環境變數

```bash
# 必需的環境變數
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
SECRET_KEY=your_secret_key

# 可選（用於指定 redirect URI）
OAUTH_REDIRECT_URI=https://yourdomain.com/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://yourdomain.com/auth/gmail/callback
```

### 6. Google Cloud Console 設定

在 Google Cloud Console 的 OAuth 同意畫面中，需要加入以下範圍：
- `openid`
- `email`
- `profile`
- `https://www.googleapis.com/auth/gmail.send`

授權的重新導向 URI 需要包含：
- `https://yourdomain.com/auth/callback` (登入用)
- `https://yourdomain.com/auth/gmail/callback` (Gmail API 用)

### 7. 檢查授權狀態

```bash
# 檢查 Gmail 授權狀態
GET /gmail/status

# 回應
{
  "is_authenticated": true/false
}
```

## 測試步驟

1. 清除 session cookies
2. 訪問 `/login` 並完成登入
3. 訪問 `/send-email`
4. 點擊"授權 Gmail API"按鈕
5. 完成 Gmail 授權
6. 應該看到"Gmail API 已授權"的綠色提示
7. 選擇模板和客戶，發送郵件
8. 郵件應該成功發送

## 常見問題

**Q: 登入後還是看不到 Gmail 授權狀態？**
A: 登入和 Gmail API 是兩個獨立的授權流程。登入後需要單獨授權 Gmail API。

**Q: 授權後還是顯示未授權？**
A: 檢查 session cookie 是否正常設置，確認 `same_site="lax"` 設定。

**Q: refresh_token 遺失？**
A: 確保在授權時有設置 `access_type='offline'` 和 `prompt='consent'`。

## 優點

✅ **職責分離**: 登入和 Gmail API 授權完全獨立  
✅ **安全性**: 即使 Gmail token 過期，用戶仍然保持登入狀態  
✅ **靈活性**: 可以單獨撤銷 Gmail API 授權而不影響登入  
✅ **易於管理**: Session 中清楚區分兩種 token
