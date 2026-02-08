# 🔧 OAuth redirect_uri 參數衝突修正

## 問題
```
TypeError: authlib.integrations.base_client.async_app.AsyncOAuth2Mixin.fetch_access_token() 
got multiple values for keyword argument 'redirect_uri'
```

## 原因

在 `authorize_access_token()` 中明確傳遞 `redirect_uri` 參數，但 Authlib 內部已經在處理這個參數，導致衝突。

## Authlib 的工作原理

### 授權階段（authorize_redirect）
```python
# 我們傳遞 redirect_uri
redirect_uri = get_redirect_uri(...)
await oauth.google.authorize_redirect(request, redirect_uri)

# Authlib 做的事：
# 1. 生成隨機 state
# 2. 將 state 和 redirect_uri 儲存在 session 中
# 3. 重定向到 Google 授權頁面
```

### 回調階段（authorize_access_token）
```python
# ❌ 錯誤：明確傳遞 redirect_uri
await oauth.google.authorize_access_token(request, redirect_uri=redirect_uri)
# Authlib 內部已經從 session 恢復 redirect_uri
# 又從 kwargs 收到 redirect_uri
# → 參數衝突！

# ✅ 正確：不傳遞 redirect_uri
await oauth.google.authorize_access_token(request)
# Authlib 做的事：
# 1. 從 session 恢復 state 和 redirect_uri
# 2. 驗證 state 是否匹配
# 3. 使用 code 和 redirect_uri 交換 token
```

## 修正方案

### Before ❌
```python
@app.get("/auth/callback")
async def auth_callback(request: Request):
    redirect_uri = get_redirect_uri(request, 'auth_callback', 'OAUTH_REDIRECT_URI')
    token = await oauth.google.authorize_access_token(request, redirect_uri=redirect_uri)
    # ❌ TypeError: got multiple values
```

### After ✅
```python
@app.get("/auth/callback")
async def auth_callback(request: Request):
    # authlib 會從 session 自動恢復 redirect_uri
    token = await oauth.google.authorize_access_token(request)
    # ✅ 正常運作
```

## 完整流程

```python
# ===== 授權流程 =====

# 1. 用戶訪問授權頁面
@app.get("/auth/login")
async def auth_login(request: Request):
    # 明確傳遞 redirect_uri（確保是 https）
    redirect_uri = get_redirect_uri(request, 'auth_callback', 'OAUTH_REDIRECT_URI')
    return await oauth.google.authorize_redirect(request, redirect_uri)
    # Authlib 儲存到 session: {'_state_google_...': {'redirect_uri': 'https://...'}}

# 2. Google 授權並返回

# 3. 回調處理
@app.get("/auth/callback")
async def auth_callback(request: Request):
    # 不傳遞 redirect_uri，讓 authlib 從 session 恢復
    token = await oauth.google.authorize_access_token(request)
    # Authlib 從 session 讀取 redirect_uri，確保一致
    
    user = token.get('userinfo')
    request.session['user'] = dict(user)
    return RedirectResponse(url='/dashboard')

# ===== Gmail 授權流程（相同邏輯）=====

@app.get("/auth/gmail/login")
async def gmail_auth_login(request: Request):
    redirect_uri = get_redirect_uri(request, 'gmail_auth_callback', 'GMAIL_OAUTH_REDIRECT_URI')
    return await oauth.google_gmail.authorize_redirect(
        request, redirect_uri,
        access_type='offline',
        prompt='consent'
    )

@app.get("/auth/gmail/callback")
async def gmail_auth_callback(request: Request):
    # 不傳遞 redirect_uri
    token = await oauth.google_gmail.authorize_access_token(request)
    
    request.session['gmail_token'] = {
        'access_token': token.get('access_token'),
        'refresh_token': token.get('refresh_token'),
        # ...
    }
    return templates.TemplateResponse("gmail_auth_success.html", {"request": request})
```

## 為什麼這樣可以避免 state mismatch？

1. **授權時**：`get_redirect_uri()` 確保使用正確的 https URI
2. **儲存時**：Authlib 將這個 URI 儲存在 session 中
3. **回調時**：Authlib 從 session 恢復完全相同的 URI
4. **結果**：redirect_uri 前後一致，state 驗證通過 ✅

## 關鍵函數：get_redirect_uri()

```python
def get_redirect_uri(request: Request, callback_name: str, env_var: str = None) -> str:
    """取得正確的 redirect_uri（優先使用環境變數，自動修正 https）"""
    
    # 優先使用環境變數（最可靠）
    if env_var:
        redirect_uri = os.getenv(env_var)
        if redirect_uri:
            return redirect_uri
    
    # 自動生成
    redirect_uri = str(request.url_for(callback_name))
    
    # Zeabur 在 proxy 後面，需要使用 https
    if 'zeabur.app' in str(request.base_url):
        redirect_uri = redirect_uri.replace('http://', 'https://')
    
    return redirect_uri
```

這個函數只在 **授權階段** 使用，確保傳遞給 Google 的 redirect_uri 是正確的。

## 測試驗證

完成修改後，檢查日誌應該看到：

```
啟動 OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/callback
開始處理 OAuth 回調
✓ 登入成功: 張三 (user@gmail.com)
```

```
啟動 Gmail API OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
開始處理 Gmail OAuth 回調
✓ Gmail API 授權成功
```

## 總結

| 階段 | 做法 | 原因 |
|------|------|------|
| 授權階段 (`authorize_redirect`) | ✅ 明確傳遞 redirect_uri | 確保使用 https，避免自動檢測錯誤 |
| 回調階段 (`authorize_access_token`) | ✅ 不傳遞 redirect_uri | 讓 authlib 從 session 恢復，避免參數衝突 |

這樣既確保了 redirect_uri 的正確性，又避免了參數衝突！
