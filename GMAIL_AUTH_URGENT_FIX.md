# 🚨 緊急修復：設定環境變數解決 State Mismatch

## 問題根源

從日誌看到 session 中有多個 state：
```
'redirect_uri': 'http://pycrm.zeabur.app/auth/gmail/callback'   ❌ 舊的
'redirect_uri': 'https://pycrm.zeabur.app/auth/gmail/callback'  ✅ 新的
```

每次授權都生成新的 state，但因為 http/https 不一致，無法匹配。

## ⚡ 立即解決方案

### 步驟 1: 在 Zeabur 設定環境變數

前往 Zeabur → 你的專案 → 環境變數，新增：

```bash
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

這樣可以強制使用 https，不依賴自動檢測。

### 步驟 2: 完全清除瀏覽器 Cookies

1. 開啟瀏覽器開發者工具（F12）
2. 前往 Application/應用程式 → Cookies
3. 刪除 `pycrm.zeabur.app` 的所有 cookies
4. 或直接清除所有瀏覽器資料：
   - Chrome: Ctrl+Shift+Delete → 全部時間 → Cookies

### 步驟 3: 重啟應用並測試

1. Zeabur 會自動重新部署
2. 使用**無痕模式**開啟瀏覽器
3. 訪問 `https://pycrm.zeabur.app/login`
4. 登入後前往 `/send-email`
5. 點擊「授權 Gmail API」

## 為什麼這樣能解決？

### Before ❌
```python
# 自動檢測，可能不一致
redirect_uri = get_redirect_uri(...)  
# 可能得到: http://pycrm.zeabur.app/...
```

### After ✅
```python
# 直接使用環境變數，永遠一致
redirect_uri = os.getenv('GMAIL_OAUTH_REDIRECT_URI')
# 永遠是: https://pycrm.zeabur.app/...
```

## 完整的環境變數設定

建議在 Zeabur 設定所有這些：

```bash
# 必需
GOOGLE_CLIENT_ID=你的client_id
GOOGLE_CLIENT_SECRET=你的client_secret  
SECRET_KEY=長隨機字串
ALLOWED_EMAILS=helpaction4u@gmail.com

# 強烈推薦（避免自動檢測問題）
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

## Google Cloud Console 確認

確保這兩個 URIs 都已添加：

```
https://pycrm.zeabur.app/auth/callback
https://pycrm.zeabur.app/auth/gmail/callback
```

## 測試檢查清單

- [ ] 設定 `GMAIL_OAUTH_REDIRECT_URI` 環境變數
- [ ] 完全清除瀏覽器 cookies
- [ ] 使用無痕模式測試
- [ ] 檢查 Zeabur 日誌：應該只看到 https URI

## 日誌應該顯示

```
使用環境變數 GMAIL_OAUTH_REDIRECT_URI: https://pycrm.zeabur.app/auth/gmail/callback
啟動 Gmail API OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
✓ Gmail API 授權成功
```

## 如果還是失敗

### 方案 A: 檢查 SECRET_KEY
```bash
# 確認 SECRET_KEY 已設定且不為空
# 在 Zeabur 環境變數中檢查
```

### 方案 B: 完全重置
1. 刪除應用並重新部署
2. 使用全新的瀏覽器設定檔
3. 確保所有環境變數都已設定

### 方案 C: 檢查瀏覽器設定
某些瀏覽器擴充套件或隱私設定會阻擋 third-party cookies：
- 停用所有擴充套件
- 檢查 Cookie 設定（允許所有 cookies）
- 使用不同的瀏覽器測試

## 為什麼會有多個 State？

每次點擊「授權 Gmail API」都會生成新的 state，如果：
1. 授權過程中沒完成就返回
2. 多次點擊授權按鈕
3. Cookie 設定有問題導致無法清理舊 state

結果就是 session 中累積多個 state，造成混淆。

**設定環境變數 + 清除 cookies = 解決問題** ✅
