# Google 登入功能實作總結

## 實作日期
2026-02-08

## 實作內容

### 1. 新增檔案
- `app/auth.py` - OAuth 認證邏輯和登入保護函數
- `app/templates/login.html` - Google 登入頁面
- `GOOGLE_LOGIN_SETUP.md` - Google OAuth 設定指南
- `verify_google_login.sh` - 功能驗證腳本

### 2. 修改檔案
- `requirements.txt` - 新增 authlib, itsdangerous, httpx
- `app/main.py` - 新增認證路由和登入保護
- `app/routers/clients.py` - API 路由添加認證保護
- `app/templates/base.html` - 添加使用者資訊顯示和登出按鈕
- `.env.example` - 新增 Google OAuth 環境變數說明
- `README.md` - 更新功能說明

### 3. 新增依賴套件
```
authlib==1.6.7
itsdangerous==2.2.0
httpx==0.28.1
```

## 功能說明

### 認證流程
1. 使用者訪問任何頁面 → 檢查是否登入
2. 未登入 → 重定向到 `/login` 登入頁
3. 點擊「使用 Google 帳號登入」→ 導向 Google OAuth
4. Google 授權後 → 回調到 `/auth/callback`
5. 儲存使用者資訊到 Session → 導向 Dashboard

### 受保護的路由
**頁面路由**（需登入才能訪問）：
- `/` - 首頁
- `/dashboard` - 控制台
- `/client/new` - 新增客戶表單
- `/client/{id}/edit` - 編輯客戶表單
- `/import` - CSV 匯入頁面

**API 路由**（需認證才能呼叫）：
- `GET /api/clients/` - 取得客戶列表
- `GET /api/clients/statistics` - 取得統計資訊
- `GET /api/clients/{id}` - 取得單一客戶
- `POST /api/clients/` - 建立客戶
- `PUT /api/clients/{id}` - 更新客戶
- `DELETE /api/clients/{id}` - 刪除客戶
- `POST /api/clients/import-csv` - 匯入 CSV

### 公開路由
- `/login` - 登入頁面
- `/auth/login` - Google OAuth 登入
- `/auth/callback` - OAuth 回調
- `/logout` - 登出

## 使用方式

### 設定步驟
1. 到 [Google Cloud Console](https://console.cloud.google.com/) 建立 OAuth 憑證
2. 在 `.env` 設定：
   ```
   GOOGLE_CLIENT_ID=你的-client-id
   GOOGLE_CLIENT_SECRET=你的-client-secret
   SECRET_KEY=隨機密鑰
   ```
3. 啟動應用程式：`uvicorn app.main:app --reload`
4. 訪問 http://localhost:8000 會自動導向登入頁

### 驗證設定
執行驗證腳本：
```bash
./verify_google_login.sh
```

## 安全性考量

1. **Session 加密**: 使用 SECRET_KEY 加密 Session 資料
2. **OAuth 2.0**: 使用 Google 標準 OAuth 2.0 流程
3. **不儲存密碼**: 僅儲存 Google 提供的使用者資訊
4. **路由保護**: 所有重要路由都需要登入
5. **HTTPS**: 生產環境建議使用 HTTPS

## 技術細節

### Session 管理
- 使用 Starlette SessionMiddleware
- Session 資料儲存在加密的 Cookie 中
- 重啟應用程式會清除 Session（需重新登入）

### 使用者資訊
儲存在 Session 中的資訊：
```python
{
    'sub': 'google-user-id',
    'name': '使用者名稱',
    'email': 'user@example.com',
    'picture': 'https://...',
    ...
}
```

### 認證檢查
兩種方式：
1. `require_login(request)` - 頁面路由，未登入返回 RedirectResponse
2. `Depends(get_current_user)` - API 路由，未登入拋出 HTTPException 401

## 後續可優化項目

1. **Remember Me**: 延長 Session 有效期
2. **角色權限**: 區分管理員和普通使用者
3. **登入記錄**: 記錄登入時間和 IP
4. **多因素認證**: 增加額外安全層
5. **Session 持久化**: 使用 Redis 或資料庫儲存 Session
6. **白名單**: 限制特定 email domain 才能登入

## 測試建議

1. 測試登入流程
2. 測試未登入訪問受保護頁面
3. 測試登出功能
4. 測試 Session 過期處理
5. 測試 API 認證保護

## 相關文件
- [GOOGLE_LOGIN_SETUP.md](GOOGLE_LOGIN_SETUP.md) - 詳細設定指南
- [README.md](README.md) - 專案說明
