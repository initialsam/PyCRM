# Email 白名單帳號管理系統

## 功能說明

系統已設定 Email 白名單機制，只有在允許名單中的 Google 帳號才能登入。

## 預設設定

預設允許登入的帳號：`helpaction4u@gmail.com`

## 如何新增允許的帳號

### 方式一：環境變數（推薦）

在 `.env` 檔案或 Zeabur 環境變數中設定 `ALLOWED_EMAILS`：

```env
# 單一帳號
ALLOWED_EMAILS=helpaction4u@gmail.com

# 多個帳號（逗號分隔）
ALLOWED_EMAILS=helpaction4u@gmail.com,user2@gmail.com,user3@example.com
```

### 方式二：Zeabur 部署環境

1. 進入 Zeabur Dashboard
2. 選擇你的專案和服務
3. 點選「Variables」（變數）
4. 新增或編輯 `ALLOWED_EMAILS` 變數
5. 重新部署服務

## 登入流程

1. 使用者點擊「使用 Google 帳號登入」
2. Google OAuth 驗證
3. **系統檢查 email 是否在白名單中**
4. ✅ 在白名單：允許登入，導向 Dashboard
5. ❌ 不在白名單：顯示「存取被拒絕」頁面

## 安全特性

- ✅ Email 檢查不區分大小寫
- ✅ 自動移除前後空格
- ✅ 拒絕登入時顯示友善的錯誤頁面
- ✅ 不會儲存未授權用戶的資訊

## 測試

### 本地測試
```bash
# 設定環境變數
export ALLOWED_EMAILS=helpaction4u@gmail.com,test@example.com

# 啟動服務
uvicorn app.main:app --reload

# 測試登入
# 使用白名單中的帳號 → 成功登入
# 使用其他帳號 → 顯示「存取被拒絕」
```

### 查看當前白名單
```python
from app.auth import get_allowed_emails
print(get_allowed_emails())
```

## 修改記錄

- ✅ `app/auth.py` - 新增 `get_allowed_emails()` 和 `is_email_allowed()` 函數
- ✅ `app/main.py` - 在 `/auth/callback` 加入白名單檢查
- ✅ `app/templates/access_denied.html` - 新增拒絕存取頁面
- ✅ `.env.example` - 新增 `ALLOWED_EMAILS` 說明

## 未來擴展

可考慮新增以下功能：
- 管理員後台管理白名單
- 資料庫存儲白名單（取代環境變數）
- Email 網域白名單（例如：允許所有 @company.com）
- 登入審計日誌
