# 📧 Gmail API 整合改進 - 使用 OAuth 憑證

## 🎯 改進概述

**重大改進**：系統現在直接使用 `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET` 環境變數來進行 Gmail API 認證，**不再需要下載 credentials.json 檔案**！

## ✨ 主要優勢

### 之前（舊版本）
- ❌ 需要從 Google Cloud Console 下載 credentials.json
- ❌ 需要將檔案放到專案根目錄
- ❌ 使用 Desktop app OAuth 類型
- ❌ 使用 `InstalledAppFlow`（本地伺服器認證）
- ❌ 部署到 Zeabur 需要手動上傳檔案
- ❌ 不適合 Web 應用

### 現在（新版本）✨
- ✅ 重用現有的 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET
- ✅ 不需要額外檔案
- ✅ 使用 Web application OAuth 類型
- ✅ 標準 OAuth 2.0 流程（redirect flow）
- ✅ 部署只需設定環境變數
- ✅ 完全適合 Web 應用

## 🔧 技術變更

### 1. 認證流程改進

#### 舊版本
```python
# 需要 credentials.json 檔案
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES
)
creds = flow.run_local_server(port=0)  # 本地伺服器
```

#### 新版本
```python
# 從環境變數讀取
client_config = {
    "web": {
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
        "redirect_uris": [redirect_uri]
    }
}
flow = Flow.from_client_config(client_config, scopes=SCOPES)
auth_url, _ = flow.authorization_url()  # Web redirect flow
```

### 2. 新增授權管理功能

```python
# 檢查授權狀態
is_authenticated() -> bool

# 取得授權 URL
get_auth_url() -> str

# 儲存授權憑證
save_credentials(auth_code: str) -> bool
```

### 3. 整合到 Web UI

- 授權狀態顯示
- 一鍵授權按鈕
- 彈窗授權流程
- 授權成功/失敗頁面

## 📝 設定步驟

### Google Cloud Console 設定

1. 選擇您的 OAuth 2.0 客戶端
2. **類型必須是**：Web application
3. 在「已授權的重新導向 URI」新增：
   ```
   http://localhost:8000/auth/callback          # 登入用
   http://localhost:8000/auth/gmail/callback    # Gmail API 用
   ```

### 環境變數（已有的）

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
```

**不需要額外設定**！Gmail API 會自動使用這些憑證。

### 首次授權

1. 登入 CRM 系統
2. 前往「發送郵件」頁面
3. 點擊「🔐 授權 Gmail API」按鈕
4. 在彈出視窗中完成 Google 授權
5. ✅ 完成！可以發送郵件

## 🎨 新增 UI 元素

### 授權狀態提示

```html
<!-- 未授權 -->
<div class="alert alert-warning">
    ⚠️ 需要 Gmail API 授權
    <button onclick="authorizeGmail()">🔐 授權 Gmail API</button>
</div>

<!-- 已授權 -->
<div class="alert alert-success">
    ✅ Gmail API 已授權，可以發送郵件
</div>
```

### 彈窗授權流程

```javascript
function authorizeGmail() {
    // 取得授權 URL
    fetch('/gmail/auth-url')
        .then(response => response.json())
        .then(data => {
            // 開啟彈窗
            window.open(data.auth_url, 'Gmail 授權', 'width=600,height=700');
        });
}
```

## 🆕 新增 API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/gmail/auth-url` | 取得 Gmail API 授權 URL |
| GET | `/auth/gmail/callback` | Gmail OAuth 回調處理 |
| GET | `/gmail/status` | 檢查授權狀態 |

## 📁 檔案變更

### 新增檔案（3 個）
- `app/templates/gmail_auth_success.html` - 授權成功頁面
- `app/templates/gmail_auth_error.html` - 授權失敗頁面
- `GMAIL_API_QUICKSTART.md` - 快速設定指南

### 修改檔案（5 個）
- `app/email_service.py` - 重構認證流程（使用 OAuth 憑證）
- `app/routers/emails.py` - 新增授權路由和狀態檢查
- `app/templates/send_email.html` - 新增授權 UI
- `.env.example` - 更新說明
- `.gitignore` - 新增 `gmail_token.pickle`

## 🔄 遷移指南

如果您之前使用 credentials.json：

1. **刪除舊檔案**（可選）：
   ```bash
   rm credentials.json token.pickle
   ```

2. **確認環境變數**：
   - `GOOGLE_CLIENT_ID` ✓
   - `GOOGLE_CLIENT_SECRET` ✓

3. **更新 Google Cloud Console**：
   - 確認 OAuth 類型是 "Web application"
   - 新增 `/auth/gmail/callback` redirect URI

4. **重新授權**：
   - 前往發送郵件頁面
   - 點擊授權按鈕
   - 完成認證

## 🚀 部署到 Zeabur

### 環境變數

在 Zeabur Dashboard 設定：
```env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
OAUTH_REDIRECT_URI=https://your-domain.zeabur.app/auth/callback
```

### Google Console 設定

新增生產環境的 redirect URIs：
```
https://your-domain.zeabur.app/auth/callback
https://your-domain.zeabur.app/auth/gmail/callback
```

### 注意事項

- Token 儲存在 `gmail_token.pickle`
- 每次重新部署後需要重新授權（因為檔案不會保留）
- 建議未來實作資料庫儲存 token 或使用持久化儲存

## ⚡ 效能與安全性

### 優勢
- ✅ 標準 OAuth 2.0 流程
- ✅ Token 自動更新
- ✅ 不儲存密碼
- ✅ 權限範圍最小化（只有 gmail.send）

### Token 管理
- Token 儲存在 `gmail_token.pickle`
- 包含 access_token 和 refresh_token
- Access token 過期會自動更新
- 已加入 `.gitignore` 保護

## 📊 對比總結

| 項目 | 舊版本 | 新版本 |
|------|--------|--------|
| 設定複雜度 | ⭐⭐⭐ | ⭐ |
| 需要額外檔案 | ✅ credentials.json | ❌ 不需要 |
| OAuth 類型 | Desktop app | Web application |
| 認證流程 | 本地伺服器 | Web redirect |
| 部署難度 | 較難 | 簡單 |
| 環境變數重用 | ❌ | ✅ |
| 適合 Web 應用 | ⚠️ | ✅ |

## 🎓 延伸閱讀

- [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
- [Gmail API Send Messages](https://developers.google.com/gmail/api/guides/sending)
- [Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2)

## 📞 快速參考

- **快速設定**：`GMAIL_API_QUICKSTART.md`
- **完整指南**：`EMAIL_SEND_GUIDE.md`
- **測試腳本**：`./test_email_setup.sh`

---

## 🎉 總結

這次改進大幅簡化了 Gmail API 的設定流程：
1. **不需要下載額外檔案**
2. **重用現有的 OAuth 憑證**
3. **更適合 Web 應用架構**
4. **部署更簡單**

現在只需在 Google Console 新增一個 redirect URI，然後點擊授權按鈕即可！🚀
