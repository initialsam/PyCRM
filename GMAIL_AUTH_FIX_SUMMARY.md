# Gmail API 授權分離 - 完成總結

## 問題描述
Gmail API 授權和用戶登入使用相同的 OAuth 配置，導致：
1. 授權衝突
2. Token 混淆
3. 發送郵件失敗

## 解決方案

### 架構改變

**之前**: 單一 OAuth 配置，混合使用
```
登入 + Gmail API → 同一個 OAuth → 衝突
```

**現在**: 雙 OAuth 配置，職責分離
```
登入     → oauth.google        → session['user']
Gmail API → oauth.google_gmail → session['gmail_token']
```

### 修改的檔案

1. **app/auth.py**
   - 新增 `google_gmail` OAuth 配置
   - Scope: `openid email profile https://www.googleapis.com/auth/gmail.send`

2. **app/main.py**
   - 新增 `/auth/gmail/login` 路由 (Gmail 授權入口)
   - 新增 `/auth/gmail/callback` 路由 (Gmail 授權回調)
   - Session 儲存 `gmail_token`

3. **app/routers/emails.py**
   - 修改 `/send-email` 檢查 session 中的 `gmail_token`
   - 修改 `/api/emails/send` 使用 session token
   - 移除舊的 `/gmail/auth-url` 和回調路由
   - 更新 `/gmail/status` 檢查邏輯

4. **app/email_service.py**
   - 新增 `set_credentials_from_token()` 方法
   - 支援從 token 字典建立憑證

5. **app/templates/send_email.html**
   - 修改 `authorizeGmail()` 函數
   - 直接導向 `/auth/gmail/login`

6. **app/templates/gmail_auth_success.html**
   - 修改成功後自動跳轉到 `/send-email`

## 使用流程

### 首次使用

1. **登入系統**
   ```
   訪問 /login → 點擊 Google 登入 → 授權基本資訊 → 重定向到 /dashboard
   ```

2. **授權 Gmail API**
   ```
   訪問 /send-email → 點擊 "授權 Gmail API" → Google 授權頁面 → 授權 gmail.send → 返回 /send-email
   ```

3. **發送郵件**
   ```
   選擇模板 → 選擇客戶 → 發送
   ```

### 後續使用

- 如果 `user` session 有效：直接訪問所有頁面
- 如果 `gmail_token` 有效：可以直接發送郵件
- 如果 `gmail_token` 過期：需要重新授權 Gmail API

## 授權 URL 對照

| 功能 | 授權入口 | 回調 URL | Session Key | 權限 |
|------|---------|---------|-------------|------|
| 用戶登入 | `/auth/login` | `/auth/callback` | `user` | `openid email profile` |
| Gmail API | `/auth/gmail/login` | `/auth/gmail/callback` | `gmail_token` | `openid email profile gmail.send` |

## Google Cloud Console 設定

**重定向 URI** (兩個都要加)：
```
https://yourdomain.com/auth/callback
https://yourdomain.com/auth/gmail/callback
```

**OAuth 範圍**：
- `openid`
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/userinfo.profile`
- `https://www.googleapis.com/auth/gmail.send`

## 環境變數

```bash
# 必需
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
SECRET_KEY=your_random_secret_key

# 可選 (如果不設置會自動生成)
OAUTH_REDIRECT_URI=https://yourdomain.com/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://yourdomain.com/auth/gmail/callback
```

## 測試檢查清單

- [ ] 可以成功登入系統
- [ ] 登入後可以訪問 `/dashboard`
- [ ] 訪問 `/send-email` 顯示"需要授權 Gmail API"
- [ ] 點擊"授權 Gmail API"按鈕導向 Google 授權頁面
- [ ] 授權後返回 `/send-email`
- [ ] 顯示"Gmail API 已授權"綠色提示
- [ ] 可以選擇模板和客戶
- [ ] 可以成功發送郵件
- [ ] 查看 `/email-logs` 確認發送記錄

## 優點

✅ **清晰分離**: 登入和 Gmail API 授權完全獨立  
✅ **更安全**: Token 分開儲存和管理  
✅ **易於除錯**: 可以分別檢查兩個授權狀態  
✅ **更靈活**: 可以單獨撤銷某一個授權  
✅ **用戶友好**: Gmail 授權失效不影響系統登入狀態

## 檔案清單

- `app/auth.py` - OAuth 配置
- `app/main.py` - 主應用和授權路由
- `app/routers/emails.py` - 郵件路由
- `app/email_service.py` - Gmail 服務
- `app/templates/send_email.html` - 發送郵件頁面
- `app/templates/gmail_auth_success.html` - 授權成功頁面
- `GMAIL_AUTH_SEPARATION.md` - 詳細說明文件
- `test_gmail_separation.sh` - 測試腳本

## 下一步

重啟應用後：
1. 清除瀏覽器 cookies
2. 重新登入
3. 授權 Gmail API
4. 測試發送郵件功能
