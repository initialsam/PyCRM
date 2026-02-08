# Zeabur 日志設定指南

## 問題
在 Zeabur 的 Runtime Logs 中看不到應用程式的日志輸出。

## 解決方案

### 1. 必須設定的環境變數

在 Zeabur Dashboard 中設定以下環境變數：

```bash
PYTHONUNBUFFERED=1
```

**作用：** 讓 Python 的輸出不被緩衝，立即顯示在日志中。

### 設定步驟：
1. 登入 Zeabur Dashboard
2. 選擇你的專案
3. 點擊 CRM 服務
4. 進入 **Variables** 標籤
5. 新增環境變數：
   - Key: `PYTHONUNBUFFERED`
   - Value: `1`
6. 點擊 **Save** 並重新部署

### 2. 已更新的檔案

以下檔案已經自動配置好以支援 Zeabur 日志：

#### `app/auth.py` 和 `app/main.py`
```python
import sys
import logging

# 配置日志 - 输出到 stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # 输出到标准输出
    ],
    force=True
)
```

#### `Procfile` 和 `zeabur.json`
```bash
# 添加 --log-level info 參數
uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info
```

### 3. 日志輸出範例

部署後，在 Zeabur Runtime Logs 中應該可以看到：

#### 應用啟動日志
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 登入相關日志
```
2026-02-08 10:30:00 - app.auth - INFO - 允許登入的 email 列表: ['helpaction4u@gmail.com']
2026-02-08 10:30:05 - app.main - INFO - 開始處理 OAuth 回調
2026-02-08 10:30:05 - app.main - INFO - 使用者嘗試登入: User Name (user@example.com)
2026-02-08 10:30:05 - app.auth - WARNING - ✗ Email 驗證失敗: user@example.com (不在白名單中)
2026-02-08 10:30:05 - app.auth - WARNING -   白名單內容: ['helpaction4u@gmail.com']
```

#### 請求日志
```
INFO:     192.168.1.1:12345 - "GET /login HTTP/1.1" 200 OK
INFO:     192.168.1.1:12345 - "GET /auth/login HTTP/1.1" 307 Temporary Redirect
INFO:     192.168.1.1:12345 - "GET /auth/callback HTTP/1.1" 200 OK
```

### 4. 驗證日志是否正常

#### 方法 1：查看 Runtime Logs
1. 進入 Zeabur Dashboard
2. 選擇你的 CRM 服務
3. 點擊 **Logs** 標籤
4. 選擇 **Runtime Logs**
5. 嘗試登入，應該會看到日志即時出現

#### 方法 2：使用 Zeabur CLI
```bash
# 安裝 Zeabur CLI
npm install -g zeabur

# 查看即時日志
zeabur logs --service crm-service --follow
```

### 5. 常見問題排查

#### 問題：還是看不到日志
**檢查項目：**
1. ✅ 確認已設定 `PYTHONUNBUFFERED=1`
2. ✅ 確認已重新部署（設定環境變數後必須重新部署）
3. ✅ 確認選擇的是 **Runtime Logs** 而非 Build Logs
4. ✅ 確認應用程式已啟動成功（檢查 Status）

**重新部署方法：**
```bash
# 方法 1：在 Dashboard 點擊 "Redeploy"
# 方法 2：推送新的 commit 觸發自動部署
git commit --allow-empty -m "Trigger redeploy"
git push
```

#### 問題：只看到 uvicorn 的日志，看不到應用程式日志
**可能原因：** 日志級別設定太高

**解決方法：**
檢查 `zeabur.json` 確保有 `--log-level info`：
```json
{
  "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info"
}
```

#### 問題：日志延遲顯示
**說明：** 這是正常的，Zeabur 的日志可能有 1-2 秒的延遲。

**建議：**
- 測試時多等待幾秒鐘
- 使用 `zeabur logs --follow` 可以獲得更即時的輸出

### 6. 本地測試日志

在本地開發時測試日志輸出：

```bash
# 啟動應用（會顯示所有日志）
source .venv/bin/activate
export PYTHONUNBUFFERED=1
uvicorn app.main:app --reload --log-level info

# 測試登入功能
python test_login_log.py
```

### 7. 日志級別說明

| 級別 | 說明 | 範例 |
|------|------|------|
| INFO | 一般資訊 | 登入成功、email 驗證通過 |
| WARNING | 警告訊息 | email 驗證失敗、不在白名單 |
| ERROR | 錯誤訊息 | OAuth 異常、資料庫錯誤 |

預設級別為 INFO，會顯示所有級別的日志。

### 8. 檢查清單

部署到 Zeabur 前的確認事項：

- [ ] 已在 Zeabur Dashboard 設定 `PYTHONUNBUFFERED=1`
- [ ] `zeabur.json` 包含 `--log-level info`
- [ ] `Procfile` 包含 `--log-level info`
- [ ] 已設定 `ALLOWED_EMAILS` 環境變數
- [ ] 已設定其他必要的環境變數（DATABASE_URL, GOOGLE_CLIENT_ID 等）
- [ ] 推送最新代碼到 Git
- [ ] 在 Zeabur 觸發重新部署
- [ ] 測試登入並檢查 Runtime Logs

## 相關文件
- `LOGIN_LOG.md` - 登入日志功能說明
- `ZEABUR_DEPLOY.md` - Zeabur 部署指南
- `.env.example` - 環境變數範例
