# 登入日志功能說明

## 問題
設定 ALLOWED_EMAILS 之後，發現該帳號也無法登入，但沒有詳細的日志記錄來診斷問題。

## 解決方案
已在系統中添加完整的日志記錄功能，包含：

### 1. 日志配置
- 在 `app/auth.py` 和 `app/main.py` 中配置 Python logging
- 日志格式：`時間 - 模組名稱 - 級別 - 訊息`
- 日志級別：INFO（正常訊息）、WARNING（警告）、ERROR（錯誤）

### 2. 登入驗證日志

#### 白名單載入日志
```
INFO - 允許登入的 email 列表: ['helpaction4u@gmail.com', 'test@example.com']
```

#### Email 驗證通過
```
INFO - ✓ Email 驗證通過: helpaction4u@gmail.com
```

#### Email 驗證失敗（不在白名單）
```
WARNING - ✗ Email 驗證失敗: notallowed@gmail.com (不在白名單中)
WARNING -   白名單內容: ['helpaction4u@gmail.com', 'test@example.com']
WARNING -   比對結果: notallowed@gmail.com not in ['helpaction4u@gmail.com', 'test@example.com']
```

### 3. OAuth 回調日志

#### 開始處理登入
```
INFO - 開始處理 OAuth 回調
INFO - 使用者嘗試登入: John Doe (john@example.com)
```

#### 登入成功
```
INFO - ✓ 登入成功: John Doe (john@example.com)
```

#### 登入被拒絕
```
WARNING - 拒絕登入: john@example.com 不在 ALLOWED_EMAILS 白名單中
```

#### 異常錯誤
```
ERROR - OAuth 回調發生異常: OAuthError: invalid_grant
```

## 測試方法

### 1. 執行測試腳本
```bash
source .venv/bin/activate
python test_login_log.py
```

### 2. 啟動伺服器並查看日志
```bash
source .venv/bin/activate
python -m uvicorn main:app --reload
```

### 3. 嘗試登入
在瀏覽器開啟 http://localhost:8000/login，嘗試使用不同的 Google 帳號登入：
- ✅ 白名單內的帳號：會看到 "Email 驗證通過" 和 "登入成功"
- ❌ 白名單外的帳號：會看到 "Email 驗證失敗" 和詳細的比對資訊

## 如何診斷登入問題

### 問題：設定的 email 無法登入

查看日志中的這幾個關鍵訊息：

1. **檢查白名單是否正確載入**
   ```
   INFO - 允許登入的 email 列表: [...]
   ```
   確認你設定的 email 是否在列表中

2. **檢查 email 比對過程**
   ```
   WARNING - ✗ Email 驗證失敗: xxx@gmail.com
   WARNING -   白名單內容: [...]
   WARNING -   比對結果: xxx@gmail.com not in [...]
   ```
   查看實際的 email 和白名單內容，可能的問題：
   - 多餘的空格：`"user@gmail.com "`（尾端有空格）
   - 拼字錯誤：`"user@gmai.com"` vs `"user@gmail.com"`
   - 大小寫問題：系統已處理（不區分大小寫）

3. **檢查環境變數設定**
   ```bash
   # 本地開發
   cat .env | grep ALLOWED_EMAILS
   
   # Zeabur 部署
   # 到 Zeabur Dashboard 檢查環境變數
   ```

## 常見問題排查

### 問題 1：email 在 ALLOWED_EMAILS 中，但還是無法登入
**解決方法：**
1. 檢查 .env 檔案中的設定是否有多餘空格
2. 重新啟動伺服器（確保新設定被載入）
3. 查看日志中的 "白名單內容" 和 "比對結果"

### 問題 2：看不到日志輸出
**解決方法：**
1. 確認使用 `uvicorn` 啟動而非背景執行
2. 設定環境變數：`export PYTHONUNBUFFERED=1`
3. 使用 Zeabur 部署時，到 Dashboard 查看 Logs

### 問題 3：多個 email 設定格式
**正確格式：**
```bash
# 用逗號分隔，無需空格
ALLOWED_EMAILS=email1@gmail.com,email2@gmail.com,email3@example.com

# 也可以有空格，系統會自動去除
ALLOWED_EMAILS=email1@gmail.com, email2@gmail.com, email3@example.com
```

## 修改的檔案
1. `app/auth.py` - 添加日志配置和驗證日志
2. `app/main.py` - 添加 OAuth 回調日志
3. `test_login_log.py` - 測試腳本（新增）
4. `LOGIN_LOG.md` - 此文件（新增）
