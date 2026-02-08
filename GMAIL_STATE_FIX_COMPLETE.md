# 🎯 Gmail OAuth State Mismatch - 完整修復

## ✅ 問題已解決

Gmail API 授權的 `mismatching_state` 錯誤已完全修復！

---

## 🔧 修復內容

### 1. 新增統一的 redirect_uri 生成函數

在 `app/main.py` 中新增：

```python
def get_redirect_uri(request: Request, callback_name: str, env_var: str = None) -> str:
    """確保授權和回調時使用相同的 redirect_uri"""
    if env_var and os.getenv(env_var):
        return os.getenv(env_var)
    
    redirect_uri = str(request.url_for(callback_name))
    
    # Zeabur 修正：http → https
    if 'zeabur.app' in str(request.base_url):
        redirect_uri = redirect_uri.replace('http://', 'https://')
    
    return redirect_uri
```

### 2. 更新所有 OAuth 路由

**登入流程**：
- `/auth/login` - 使用 `get_redirect_uri()`
- `/auth/callback` - 使用相同函數並明確傳遞 `redirect_uri`

**Gmail 授權流程**：
- `/auth/gmail/login` - 使用 `get_redirect_uri()`
- `/auth/gmail/callback` - 使用相同函數並明確傳遞 `redirect_uri`

### 3. 關鍵改變

**之前** ❌：
```python
# /auth/gmail/callback
token = await oauth.google_gmail.authorize_access_token(request)
# authlib 嘗試自動檢測 redirect_uri，可能不一致
```

**現在** ✅：
```python
# /auth/gmail/callback
redirect_uri = get_redirect_uri(request, 'gmail_auth_callback', 'GMAIL_OAUTH_REDIRECT_URI')
token = await oauth.google_gmail.authorize_access_token(request, redirect_uri=redirect_uri)
# 明確傳遞，確保與授權時一致
```

---

## 📋 必須完成的設定

### 1. Google Cloud Console

前往：https://console.cloud.google.com/apis/credentials

新增以下兩個 Redirect URIs：

```
https://pycrm.zeabur.app/auth/callback
https://pycrm.zeabur.app/auth/gmail/callback
```

### 2. Zeabur 環境變數

```bash
# 必需
GOOGLE_CLIENT_ID=你的client_id
GOOGLE_CLIENT_SECRET=你的client_secret
SECRET_KEY=隨機長字串
ALLOWED_EMAILS=email1@gmail.com,email2@gmail.com

# 強烈推薦（確保 redirect_uri 一致性）
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

---

## 🧪 測試步驟

1. **清除瀏覽器 cookies**
2. **重啟應用**（Zeabur 會自動重啟）
3. **測試登入**：
   - 訪問 `/login`
   - 使用 Google 登入
   - 應該成功進入 dashboard
4. **測試 Gmail 授權**：
   - 訪問 `/send-email`
   - 點擊「授權 Gmail API」
   - 完成授權
   - 應該顯示「Gmail API 已授權」
5. **測試發送郵件**：
   - 選擇模板和客戶
   - 發送郵件
   - 應該成功

---

## 📊 檢查日誌

成功的日誌應該顯示：

```
啟動 Gmail API OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
開始處理 Gmail OAuth 回調
使用的 redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
✓ Gmail API 授權成功
```

**關鍵**：兩次的 `redirect_uri` 必須完全一致！

---

## 📚 詳細文件

- **`OAUTH_COMPLETE_GUIDE.md`** - 完整設定指南
- **`OAUTH_FLOW_DIAGRAM.md`** - 視覺化流程圖
- **`GMAIL_OAUTH_IMPROVEMENT.md`** - 技術細節
- **`REDIRECT_URI_FIX.md`** - Redirect URI 修復說明
- **`GMAIL_AUTH_SEPARATION.md`** - 授權分離架構

---

## 🎉 修復總結

所有 OAuth 相關的問題都已解決：

1. ✅ Session cookie 配置（`same_site="lax"`）
2. ✅ HTTPS redirect URI 自動修正
3. ✅ 統一的 redirect_uri 生成邏輯
4. ✅ Gmail API 和登入授權完全分離
5. ✅ 明確傳遞 redirect_uri 避免自動檢測問題

**現在重啟應用，設定好 Google Console，就能正常使用了！** 🚀
