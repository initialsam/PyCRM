# Session Cookie 配置強化 - State Mismatch 最終修復

## 問題
Gmail OAuth 仍然出現：
```
mismatching_state: CSRF Warning! State not equal in request and response.
```

## 根本原因

在 HTTPS proxy 環境（如 Zeabur）中，session cookie 需要特殊配置才能在 OAuth redirect 期間正確保持。

## 修改內容

### 1. Session Cookie 配置改為 `same_site="none"`

```python
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    session_cookie="session",
    max_age=3600,
    same_site="none",   # ← 從 "lax" 改為 "none"
    https_only=True,    # ← 從 False 改為 True
    path="/"
)
```

**為什麼？**
- `same_site="lax"` 在某些 OAuth redirect 情況下會阻擋 cookie
- `same_site="none"` 允許跨站點傳送 cookie，但**必須**配合 `https_only=True`
- Zeabur 使用 HTTPS，所以 `https_only=True` 是正確的

### 2. 添加 TrustedHostMiddleware

```python
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["pycrm.zeabur.app", "*.zeabur.app", "localhost", "127.0.0.1"]
)
```

**為什麼？**
- Zeabur 在 proxy 後面，需要信任 proxy headers
- 確保 request.base_url 正確解析

### 3. 增強調試日誌

在 `/auth/gmail/login` 和 `/auth/gmail/callback` 添加詳細日誌：
- Request headers (Host, X-Forwarded-Proto)
- Session ID
- Session data

這樣可以追蹤 session 是否在兩次請求之間保持一致。

## Cookie SameSite 屬性說明

| 值 | 說明 | OAuth 可用 | 需要 HTTPS |
|----|------|-----------|-----------|
| `strict` | 完全不允許跨站點 | ❌ | - |
| `lax` | 允許 top-level navigation | ⚠️ 有時可以 | - |
| `none` | 完全允許跨站點 | ✅ | ✅ 必須 |

### OAuth Flow 的 Cookie 行為

```
你的網站 (pycrm.zeabur.app)
    ↓ 用戶點擊授權
Google 授權頁面 (accounts.google.com)
    ↓ 用戶授權
你的網站 callback (pycrm.zeabur.app/auth/gmail/callback)
```

在這個流程中：
- **same_site="strict"**: Cookie 不會被送回 ❌
- **same_site="lax"**: 可能會被送回（取決於瀏覽器實現）⚠️
- **same_site="none" + https_only=True**: Cookie 會被送回 ✅

## 測試日誌

重啟應用後，查看日誌應該顯示：

```
啟動 Gmail API OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
Request headers - Host: pycrm.zeabur.app, X-Forwarded-Proto: https
Session ID before: abc123
Session data before: {'_id': 'abc123', ...}

[用戶在 Google 授權]

開始處理 Gmail OAuth 回調
Request headers - Host: pycrm.zeabur.app, X-Forwarded-Proto: https
Session ID after: abc123  ← 應該和 before 一樣！
Session data after: {'_id': 'abc123', '_state_google_gmail_...': {...}}
Session keys: ['_id', '_state_google_gmail_...']
✓ Gmail API 授權成功
```

**關鍵檢查點**：
- Session ID 前後一致
- Session data 中有 `_state_google_gmail_...` 鍵
- X-Forwarded-Proto 是 `https`

## 如果還是失敗

### 檢查 1: SECRET_KEY
```bash
# 確認 SECRET_KEY 已設定且不為空
echo $SECRET_KEY
```

### 檢查 2: 清除瀏覽器
完全清除瀏覽器的 cookies 和 cache：
```
Chrome: Ctrl+Shift+Delete → 全部時間 → Cookies 和 Cache
```

### 檢查 3: 檢查日誌中的 Session ID
如果 "before" 和 "after" 的 Session ID 不一樣，表示 cookie 沒有保持。可能原因：
- 瀏覽器阻擋第三方 cookie
- SECRET_KEY 改變了
- Cookie domain 設定問題

### 檢查 4: 使用無痕模式測試
在無痕/隱私模式中測試，排除瀏覽器擴充套件干擾。

## 瀏覽器兼容性

| 瀏覽器 | SameSite=None 支援 |
|--------|-------------------|
| Chrome 80+ | ✅ |
| Firefox 69+ | ✅ |
| Safari 13+ | ✅ |
| Edge 86+ | ✅ |

如果使用較舊的瀏覽器，可能不支援 `SameSite=None`。

## 環境變數確認

```bash
# 必須設定
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
SECRET_KEY=... # ← 必須是長隨機字串，不能為空
ALLOWED_EMAILS=...

# 推薦設定
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

## 修改文件

- `app/main.py`
  - 更新 SessionMiddleware: `same_site="none"`, `https_only=True`
  - 新增 TrustedHostMiddleware
  - 增強 `/auth/gmail/login` 和 `/auth/gmail/callback` 的日誌

## 下一步

1. 重啟應用
2. 完全清除瀏覽器 cookies
3. 測試 Gmail 授權
4. 檢查日誌確認 Session ID 一致
5. 如果成功，應該能看到「Gmail API 授權成功」

這次的修改針對 HTTPS proxy 環境做了特別優化，應該能解決 state mismatch 問題！
