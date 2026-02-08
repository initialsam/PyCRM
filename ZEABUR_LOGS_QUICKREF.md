# Zeabur 日志快速參考

## ⚡ 快速修復步驟

### 1️⃣ 在 Zeabur Dashboard 設定環境變數
```
PYTHONUNBUFFERED=1
```

### 2️⃣ 儲存並重新部署
- 點擊 **Save**
- 點擊 **Redeploy**

### 3️⃣ 查看日志
- 進入 **Logs** 標籤
- 選擇 **Runtime Logs**（不是 Build Logs）

## 📋 預期看到的日志

### ✅ 正常啟動
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### ✅ 白名單載入
```
2026-02-08 10:30:00 - app.auth - INFO - 允許登入的 email 列表: ['helpaction4u@gmail.com']
```

### ✅ 登入成功
```
2026-02-08 10:30:05 - app.main - INFO - 開始處理 OAuth 回調
2026-02-08 10:30:05 - app.main - INFO - 使用者嘗試登入: User Name (user@gmail.com)
2026-02-08 10:30:05 - app.auth - INFO - ✓ Email 驗證通過: user@gmail.com
2026-02-08 10:30:05 - app.main - INFO - ✓ 登入成功: User Name (user@gmail.com)
```

### ⚠️ 登入失敗（不在白名單）
```
2026-02-08 10:30:05 - app.auth - WARNING - ✗ Email 驗證失敗: user@example.com (不在白名單中)
2026-02-08 10:30:05 - app.auth - WARNING -   白名單內容: ['helpaction4u@gmail.com']
2026-02-08 10:30:05 - app.auth - WARNING -   比對結果: user@example.com not in ['helpaction4u@gmail.com']
```

## 🔍 故障排除

### 問題：還是看不到日志

**檢查清單：**
- [ ] 已設定 `PYTHONUNBUFFERED=1`
- [ ] 已點擊 **Save** 儲存環境變數
- [ ] 已點擊 **Redeploy** 重新部署
- [ ] 正在查看 **Runtime Logs**（不是 Build Logs）
- [ ] 應用程式狀態為 **Running**
- [ ] 已嘗試登入（觸發日志輸出）

### 問題：日志延遲

這是正常的，Zeabur 的日志可能有 1-2 秒延遲。

### 問題：只看到 uvicorn 日志

確認 `zeabur.json` 包含：
```json
"startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info"
```

## 🧪 本地測試

```bash
# 檢查配置
./check_zeabur_logs.sh

# 測試日志輸出
source .venv/bin/activate
export PYTHONUNBUFFERED=1
python test_login_log.py
```

## 📖 完整文檔
- `ZEABUR_LOGS_SETUP.md` - 詳細設定指南
- `LOGIN_LOG.md` - 登入日志功能說明
