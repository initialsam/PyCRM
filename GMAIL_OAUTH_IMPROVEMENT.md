# Gmail OAuth State Mismatch 修復

## 問題
Gmail API 授權失敗，錯誤訊息：
```
mismatching_state: CSRF Warning! State not equal in request and response.
```

## 根本原因

OAuth 2.0 的 state 參數用於防止 CSRF 攻擊。問題出在：

1. **redirect_uri 不一致**：`authorize_redirect` 和 `authorize_access_token` 必須使用完全相同的 redirect_uri
2. **http vs https**：在 Zeabur (proxy 後面) 自動生成的 URL 可能是 http，但實際需要 https

## 解決方案

### 1. 創建統一的 redirect_uri 生成函數

```python
def get_redirect_uri(request: Request, callback_name: str, env_var: str = None) -> str:
    """
    取得正確的 redirect_uri
    確保在授權和回調時使用完全相同的 URI
    """
    # 優先使用環境變數（推薦）
    if env_var:
        redirect_uri = os.getenv(env_var)
        if redirect_uri:
            return redirect_uri
    
    # 自動生成
    redirect_uri = str(request.url_for(callback_name))
    
    # Zeabur 修正：使用 https
    if 'zeabur.app' in str(request.base_url):
        redirect_uri = redirect_uri.replace('http://', 'https://')
    
    return redirect_uri
```

### 2. 在 authorize_redirect 時使用

```python
@app.get("/auth/gmail/login")
async def gmail_auth_login(request: Request):
    redirect_uri = get_redirect_uri(request, 'gmail_auth_callback', 'GMAIL_OAUTH_REDIRECT_URI')
    
    return await oauth.google_gmail.authorize_redirect(
        request, 
        redirect_uri,
        access_type='offline',
        prompt='consent'
    )
```

### 3. 在 authorize_access_token 時讓 authlib 自動處理

```python
@app.get("/auth/gmail/callback")
async def gmail_auth_callback(request: Request):
    # authlib 會從 session 中自動恢復 redirect_uri
    # 不需要明確傳遞，這樣可以確保使用相同的值
    token = await oauth.google_gmail.authorize_access_token(request)
```

## 關鍵點

### ✅ 正確做法
```python
# Step 1: 授權時 - 明確傳遞 redirect_uri
redirect_uri = get_redirect_uri(...)
oauth.authorize_redirect(request, redirect_uri)
# authlib 將 redirect_uri 儲存在 session 中

# Step 2: 回調時 - 讓 authlib 從 session 恢復
oauth.authorize_access_token(request)  # 不傳遞 redirect_uri
# authlib 自動使用 session 中的值，確保一致
```

### ❌ 錯誤做法
```python
# 錯誤 1: 在回調時明確傳遞 redirect_uri
token = await oauth.authorize_access_token(request, redirect_uri=redirect_uri)
# ❌ TypeError: got multiple values for keyword argument 'redirect_uri'

# 錯誤 2: 授權時不傳遞 redirect_uri
oauth.authorize_redirect(request)  # 讓它自動檢測
# ❌ 可能檢測到 http:// 而不是 https://
```

## 為什麼之前會失敗？

### 問題 1: 授權時未明確指定 redirect_uri

1. **授權階段** (`/auth/gmail/login`)：
   - 沒有明確傳遞 redirect_uri
   - Authlib 自動檢測：`http://pycrm.zeabur.app/auth/gmail/callback`
   - 儲存在 session 中

2. **回調階段** (`/auth/gmail/callback`)：
   - Authlib 從 session 恢復：`http://pycrm.zeabur.app/auth/gmail/callback`
   - 但 Google 返回的是：`https://pycrm.zeabur.app/auth/gmail/callback`
   - redirect_uri 不一致 → state 驗證失敗

### 問題 2: 在回調時重複傳遞 redirect_uri

```python
# ❌ 錯誤
token = await oauth.authorize_access_token(request, redirect_uri=redirect_uri)
# TypeError: got multiple values for keyword argument 'redirect_uri'
```

Authlib 內部已經有處理 redirect_uri 的邏輯，我們不應該再次傳遞。

### ✅ 正確做法

1. **授權時明確傳遞** redirect_uri（使用 `get_redirect_uri()` 確保 https）
2. **回調時不傳遞** redirect_uri（讓 authlib 從 session 自動恢復）
3. **確保一致性**：session 儲存和恢復的是同一個值

## 環境變數設定（推薦）

為了避免自動檢測的問題，建議在 Zeabur 設定環境變數：

```bash
# 用戶登入
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback

# Gmail API
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

這樣可以確保：
- redirect_uri 始終一致
- 不依賴自動檢測
- 更容易除錯

## Session 配置

確保 SessionMiddleware 配置正確（已在之前修復）：

```python
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    session_cookie="session",
    max_age=3600,
    same_site="lax",  # 重要：允許 OAuth redirect
    https_only=False   # 開發環境 False，生產環境可設為 True
)
```

## 測試清單

- [ ] 設定環境變數（OAUTH_REDIRECT_URI, GMAIL_OAUTH_REDIRECT_URI）
- [ ] 重啟應用
- [ ] 清除瀏覽器 cookies
- [ ] 測試登入流程 (`/auth/login`)
- [ ] 測試 Gmail 授權流程 (`/auth/gmail/login`)
- [ ] 檢查日誌確認 redirect_uri 一致

## 日誌範例

成功的日誌應該看起來像這樣：

```
啟動 Gmail API OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
開始處理 Gmail OAuth 回調
使用的 redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
✓ Gmail API 授權成功
```

注意兩次的 redirect_uri 必須完全一致。

## 修改的文件

- `app/main.py`
  - 新增 `get_redirect_uri()` 輔助函數（確保授權時使用正確的 https URI）
  - 更新 `/auth/login` 使用輔助函數明確傳遞 redirect_uri
  - 更新 `/auth/callback` **不傳遞** redirect_uri（讓 authlib 自動處理）
  - 更新 `/auth/gmail/login` 使用輔助函數明確傳遞 redirect_uri
  - 更新 `/auth/gmail/callback` **不傳遞** redirect_uri（讓 authlib 自動處理）

## 關鍵要點

1. ✅ **授權時**：使用 `get_redirect_uri()` 明確傳遞 redirect_uri
2. ✅ **回調時**：不傳遞 redirect_uri，讓 authlib 從 session 恢復
3. ✅ **Zeabur 環境**：自動將 http 轉換為 https
4. ✅ **一致性保證**：authlib 確保使用相同的 redirect_uri

## 相關文件

- `OAUTH_STATE_FIX.md` - 最初的 OAuth state 問題修復
- `GMAIL_AUTH_SEPARATION.md` - Gmail API 授權分離說明
- `REDIRECT_URI_FIX.md` - Redirect URI 不匹配問題
