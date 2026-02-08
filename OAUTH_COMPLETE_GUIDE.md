# 🎯 OAuth 完整設定指南 - 最終版本

## ✅ 所有問題已修復

1. ✅ Session cookie 配置（same_site="lax"）
2. ✅ HTTPS redirect URI 自動修正
3. ✅ 統一的 redirect_uri 生成邏輯
4. ✅ Gmail API 和登入授權分離

---

## 🔧 必需的 Zeabur 環境變數

```bash
# === 必需 ===
GOOGLE_CLIENT_ID=你的_client_id
GOOGLE_CLIENT_SECRET=你的_client_secret
SECRET_KEY=隨機長字串_至少32字元
ALLOWED_EMAILS=email1@gmail.com,email2@gmail.com

# === 強烈推薦（避免自動檢測問題）===
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

---

## 🌐 Google Cloud Console 設定

### 1. 前往 OAuth 2.0 客戶端設定
🔗 https://console.cloud.google.com/apis/credentials

### 2. 編輯你的 OAuth 2.0 客戶端 ID

### 3. 已授權的重新導向 URI（兩個都要加）

```
https://pycrm.zeabur.app/auth/callback
https://pycrm.zeabur.app/auth/gmail/callback
```

⚠️ **注意**：
- 必須是 `https://`（不是 http）
- URI 結尾不要有 `/`
- 必須完全一致

### 4. OAuth 同意畫面 - 範圍設定

確保包含以下範圍：
- `openid`
- `.../auth/userinfo.email`
- `.../auth/userinfo.profile`
- `.../auth/gmail.send`

### 5. 測試使用者（如果應用未發布）

新增允許的測試使用者 email。

---

## 🧪 測試步驟

### 步驟 1: 清除狀態
```bash
# 清除瀏覽器 cookies 和快取
Ctrl+Shift+Delete (Chrome/Edge)
Cmd+Shift+Delete (Mac)
```

### 步驟 2: 測試登入
1. 訪問 `https://pycrm.zeabur.app/login`
2. 點擊「使用 Google 登入」
3. 選擇帳號並授權
4. 應該重定向到 `/dashboard`
5. ✅ 檢查是否成功登入

### 步驟 3: 測試 Gmail API 授權
1. 訪問 `https://pycrm.zeabur.app/send-email`
2. 應該看到「需要 Gmail API 授權」警告
3. 點擊「🔐 授權 Gmail API」按鈕
4. Google 授權頁面會再次出現（這次是授權 gmail.send）
5. 授權後應該返回 `/send-email`
6. ✅ 檢查是否顯示「Gmail API 已授權」

### 步驟 4: 測試發送郵件
1. 選擇一個郵件模板
2. 選擇一個或多個客戶
3. 點擊「發送郵件」
4. ✅ 應該成功發送

---

## 📊 檢查日誌

在 Zeabur 日誌中應該看到：

### 成功的登入流程
```
啟動 OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/callback
開始處理 OAuth 回調
使用的 redirect_uri: https://pycrm.zeabur.app/auth/callback
使用者嘗試登入: 張三 (user@gmail.com)
✓ 登入成功: 張三 (user@gmail.com)
```

### 成功的 Gmail 授權流程
```
啟動 Gmail API OAuth 流程，redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
開始處理 Gmail OAuth 回調
使用的 redirect_uri: https://pycrm.zeabur.app/auth/gmail/callback
✓ Gmail API 授權成功
```

⚠️ **關鍵**：兩次的 redirect_uri 必須完全一致！

---

## 🚨 常見問題排除

### 問題 1: redirect_uri_mismatch
**症狀**: Google 顯示「這個應用程式不符合 OAuth 2.0 政策」

**解決**:
1. 檢查 Google Console 的 Redirect URIs 是否包含兩個 URIs
2. 確認使用 `https://` 不是 `http://`
3. 等待 5-10 分鐘讓 Google 更新設定
4. 清除瀏覽器 cookies

### 問題 2: mismatching_state
**症狀**: CSRF Warning! State not equal

**解決**:
1. 確認已設定環境變數 `OAUTH_REDIRECT_URI` 和 `GMAIL_OAUTH_REDIRECT_URI`
2. 確認 `SECRET_KEY` 已設定且不為空
3. 重啟應用
4. 清除瀏覽器 cookies
5. 檢查日誌確認兩次的 redirect_uri 一致

### 問題 3: Gmail API 未授權
**症狀**: 發送郵件時提示未授權

**解決**:
1. 訪問 `/send-email`
2. 點擊「授權 Gmail API」按鈕
3. 完成授權流程
4. 檢查 `/gmail/status` 確認授權狀態

### 問題 4: 白名單錯誤
**症狀**: 登入後顯示「存取被拒」

**解決**:
1. 檢查 `ALLOWED_EMAILS` 環境變數
2. 確認 email 格式正確（逗號分隔，無空格）
3. 重啟應用

---

## 📝 環境變數快速複製

```bash
# 複製以下內容到 Zeabur 環境變數設定
GOOGLE_CLIENT_ID=你的client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=你的client_secret
SECRET_KEY=請生成一個長隨機字串
ALLOWED_EMAILS=your-email@gmail.com
OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/callback
GMAIL_OAUTH_REDIRECT_URI=https://pycrm.zeabur.app/auth/gmail/callback
```

---

## 🎉 成功標誌

當所有設定正確時，你應該能：

- ✅ 使用 Google 帳號登入系統
- ✅ 訪問 dashboard 和所有頁面
- ✅ 在 send-email 頁面看到「Gmail API 已授權」
- ✅ 成功發送郵件給客戶
- ✅ 在 email-logs 看到發送記錄

---

## 📚 相關文件

- `OAUTH_STATE_FIX.md` - OAuth state 問題原始修復
- `GMAIL_AUTH_SEPARATION.md` - Gmail API 授權分離說明
- `REDIRECT_URI_FIX.md` - Redirect URI 問題修復
- `GMAIL_OAUTH_IMPROVEMENT.md` - 統一 redirect_uri 邏輯
- `QUICKFIX_REDIRECT_URI.md` - 快速參考卡

---

## 🔍 驗證腳本

執行以下腳本檢查設定：

```bash
./setup_oauth_uris.sh
```

這會顯示需要設定的 URIs 和環境變數狀態。

---

## ✨ 完成！

所有 OAuth 相關的問題都已修復。重啟應用後應該能正常運作！
