# 📧 使用 Google OAuth 憑證發送 Gmail - 快速指南

## 🎯 重大改進

**不再需要下載 credentials.json！** 系統現在直接使用您的 `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET` 來發送郵件。

## ⚡ 3 步驟快速設定

### 步驟 1：在 Google Cloud Console 新增 Redirect URI

1. 前往 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. 選擇您的 OAuth 2.0 客戶端 ID
3. 在「已授權的重新導向 URI」**新增**：
   ```
   http://localhost:8000/auth/gmail/callback
   ```
   （如果是生產環境，使用 `https://your-domain.com/auth/gmail/callback`）

4. 在「已授權的 redirect URIs」確認有兩個：
   - `http://localhost:8000/auth/callback` （登入用）
   - `http://localhost:8000/auth/gmail/callback` （Gmail API 用）

### 步驟 2：確認環境變數

`.env` 檔案中已經有：
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
```

**不需要額外設定**，Gmail API 會自動使用這些憑證！

### 步驟 3：首次授權

1. 啟動應用：`uvicorn app.main:app --reload`
2. 登入系統後，進入 Dashboard
3. 點擊「📧 發送郵件」
4. 看到「需要 Gmail API 授權」提示
5. 點擊「🔐 授權 Gmail API」按鈕
6. 瀏覽器會開啟新視窗進行 Google 認證
7. 選擇您的 Google 帳號並允許權限
8. 授權完成後視窗自動關閉
9. ✅ 完成！現在可以發送郵件了

## 🔍 詳細說明

### 授權流程

```
1. 使用者點擊「授權 Gmail API」
   ↓
2. 系統使用 GOOGLE_CLIENT_ID 生成授權 URL
   ↓
3. 開啟新視窗，使用者登入 Google 並授權
   ↓
4. Google 重新導向到 /auth/gmail/callback 並附上授權碼
   ↓
5. 系統用授權碼 + GOOGLE_CLIENT_SECRET 交換 access token
   ↓
6. Token 儲存到 gmail_token.pickle
   ↓
7. ✅ 完成！可以發送郵件
```

### 需要的 Google API 權限

確認在 Google Cloud Console 中啟用：
- ✅ Gmail API

需要的 OAuth Scope：
- ✅ `https://www.googleapis.com/auth/gmail.send`

### 與登入系統的關係

| 功能 | 使用的 Redirect URI | 用途 |
|------|-------------------|------|
| 系統登入 | `/auth/callback` | 使用 Google 帳號登入 CRM |
| Gmail 發送 | `/auth/gmail/callback` | 授權發送郵件 |

**兩者使用相同的 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET！**

## 🎨 使用流程

### 發送郵件

1. Dashboard → 點擊「📧 發送郵件」
2. 如果未授權，點擊「授權 Gmail API」（只需一次）
3. 授權完成後：
   - 選擇郵件模板
   - 選擇收件客戶
   - 點擊「發送郵件」
4. 查看發送結果

### 查看發送記錄

Dashboard → 點擊「📬 發送記錄」

## 🔒 安全性

- ✅ Token 儲存在本地（`gmail_token.pickle`）
- ✅ 已加入 `.gitignore`，不會上傳到 Git
- ✅ 使用 OAuth 2.0 標準認證
- ✅ 不需要儲存 Gmail 密碼

## ⚠️ 故障排除

### 問題 1：找不到授權 URL
**解決**：確認環境變數 `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET` 已設定

### 問題 2：授權後顯示錯誤
**解決**：
1. 確認 Google Cloud Console 已新增 `/auth/gmail/callback`
2. 確認 OAuth 客戶端類型是「Web application」
3. 確認 Gmail API 已啟用

### 問題 3：Token 過期
**解決**：
1. 刪除 `gmail_token.pickle`
2. 重新進行授權流程

### 問題 4：發送失敗
**解決**：
1. 檢查授權狀態：訪問 `/gmail/status`
2. 查看發送記錄中的錯誤訊息
3. 確認收件人 Email 格式正確

## 📦 部署到 Zeabur

### 環境變數設定

在 Zeabur Dashboard 設定：
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
OAUTH_REDIRECT_URI=https://your-domain.zeabur.app/auth/callback
```

### Google Cloud Console 設定

在「已授權的重新導向 URI」新增：
```
https://your-domain.zeabur.app/auth/callback
https://your-domain.zeabur.app/auth/gmail/callback
```

### 注意事項

- ⚠️ `gmail_token.pickle` 不會部署到 Zeabur
- ⚠️ 每次重新部署需要重新授權一次
- ✅ 建議使用持久化儲存來保存 token（未來改進）

## 🎉 優勢

相比舊版本（需要 credentials.json）：

| 項目 | 舊版本 | 新版本 ✨ |
|------|--------|---------|
| 設定檔案 | 需要下載 credentials.json | ❌ 不需要 |
| 環境變數 | 需要額外設定 | ✅ 重用現有的 |
| 部署複雜度 | 需要上傳檔案 | ✅ 只需環境變數 |
| OAuth 類型 | Desktop app | ✅ Web application |
| Zeabur 部署 | 較複雜 | ✅ 簡單 |

## 📝 總結

1. **不需要 credentials.json**
2. **使用現有的 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET**
3. **只需在 Google Console 新增一個 Redirect URI**
4. **首次使用點擊授權按鈕即可**

簡單、快速、容易部署！🚀

---

**完整文件**：參考 `EMAIL_SEND_GUIDE.md`
