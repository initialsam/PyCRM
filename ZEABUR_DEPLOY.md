# 🚀 Zeabur 部署指南

## 📋 部署前準備

### 1. 確認檔案已建立
✅ `requirements.txt` - Python 依賴套件
✅ `Dockerfile` - Docker 容器配置
✅ `Procfile` - 啟動命令
✅ `zeabur.json` - Zeabur 配置
✅ `.env.example` - 環境變數範例

## 🌐 Zeabur 部署步驟

### 方法 A：使用 GitHub 部署（推薦）

#### 1. 推送程式碼到 GitHub
```bash
cd /mnt/n/vibe/CRM

# 初始化 Git（如果還沒有）
git init
git add .
git commit -m "Initial commit for Zeabur deployment"

# 推送到 GitHub
git remote add origin https://github.com/your-username/crm.git
git branch -M main
git push -u origin main
```

#### 2. 在 Zeabur 建立專案
1. 訪問 [Zeabur Dashboard](https://dash.zeabur.com)
2. 點擊 "Create Project"
3. 選擇 "Deploy from GitHub"
4. 選擇你的 CRM repository

#### 3. 添加 PostgreSQL 服務
1. 在專案中點擊 "Add Service"
2. 選擇 "PostgreSQL"
3. 等待 PostgreSQL 啟動完成
4. Zeabur 會自動注入 `POSTGRES_URL` 環境變數

#### 4. 配置環境變數
在應用服務中設定：
```
DATABASE_URL=${POSTGRES_URL}
```

或手動設定完整連線字串：
```
DATABASE_URL=postgresql://postgres:password@postgres.zeabur.internal:5432/crm_db
```

#### 5. 部署應用
- Zeabur 會自動偵測 `Dockerfile` 並開始構建
- 等待構建完成
- 應用會自動啟動

### 方法 B：使用 CLI 部署

#### 1. 安裝 Zeabur CLI
```bash
npm install -g @zeabur/cli
```

#### 2. 登入
```bash
zeabur auth login
```

#### 3. 部署
```bash
cd /mnt/n/vibe/CRM
zeabur deploy
```

## 🔧 重要配置說明

### 資料庫配置

#### 選項 1：使用 Zeabur PostgreSQL（推薦）
Zeabur 會自動提供：
- `POSTGRES_URL` - 完整連線字串
- `POSTGRES_HOST` - 主機位址
- `POSTGRES_PORT` - 端口
- `POSTGRES_USER` - 用戶名
- `POSTGRES_PASSWORD` - 密碼
- `POSTGRES_DATABASE` - 資料庫名稱

在 `app/database.py` 中修改：
```python
import os

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
```

#### 選項 2：使用外部資料庫
手動設定 `DATABASE_URL` 環境變數

### 端口配置
Zeabur 會自動注入 `PORT` 環境變數，應用需要監聽此端口。

現在的配置已經處理：
```python
# Procfile
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### 靜態檔案
Zeabur 會自動處理靜態檔案路由，無需額外配置。

## 📝 修改建議

### 1. 修改 `app/database.py`
```python
import os

# 支援 Zeabur 的環境變數
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "postgresql://postgres:postgres@localhost:5432/crm_db"

engine = create_engine(DATABASE_URL)
```

### 2. 修改 `app/main.py`
```python
import os

# ... 現有程式碼 ...

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## 🐛 常見問題排解

### 問題 1：應用無法啟動
**檢查**：
1. 查看 Zeabur 的 Build Logs
2. 確認 `requirements.txt` 包含所有依賴
3. 檢查啟動命令是否正確

### 問題 2：資料庫連線失敗
**解決**：
1. 確認 PostgreSQL 服務已啟動
2. 檢查 `DATABASE_URL` 環境變數
3. 確認資料庫連線字串格式正確

```bash
# 正確格式
postgresql://username:password@host:port/database
```

### 問題 3：靜態檔案 404
**解決**：
確認 `app/main.py` 中有正確掛載靜態檔案：
```python
app.mount("/static", StaticFiles(directory="app/static"), name="static")
```

### 問題 4：端口綁定錯誤
**解決**：
確認應用監聽 `$PORT` 環境變數：
```python
port = int(os.getenv("PORT", 8000))
```

## 📊 部署後檢查

### 1. 健康檢查
訪問：`https://your-app.zeabur.app/docs`

### 2. 測試 API
```bash
curl https://your-app.zeabur.app/api/clients/statistics
```

### 3. 測試 Dashboard
訪問：`https://your-app.zeabur.app/dashboard`

### 4. 檢查資料庫
在 Zeabur Dashboard 中打開 PostgreSQL 的 Web Terminal：
```sql
\c crm_db
SELECT * FROM clients;
```

## 🔄 更新部署

### 使用 GitHub（自動部署）
```bash
git add .
git commit -m "Update"
git push
```
Zeabur 會自動偵測並重新部署

### 使用 CLI
```bash
zeabur deploy
```

## 📁 最終檢查清單

部署前確認：
- [ ] `requirements.txt` 已生成
- [ ] `Dockerfile` 已建立
- [ ] `Procfile` 已建立
- [ ] `.gitignore` 包含 `.env`
- [ ] 程式碼已推送到 GitHub
- [ ] Zeabur 專案已建立
- [ ] PostgreSQL 服務已添加
- [ ] 環境變數已設定
- [ ] 應用已成功部署

## 🎉 部署成功

部署成功後，你的 CRM 系統將可通過以下網址訪問：
```
https://your-app-name.zeabur.app
```

### 功能驗證
- ✅ Dashboard: `/dashboard`
- ✅ API 文件: `/docs`
- ✅ 新增客戶: `/client/new`
- ✅ CSV 匯入: `/import`

## 📞 需要幫助？

- [Zeabur 文件](https://zeabur.com/docs)
- [Zeabur Discord](https://discord.gg/zeabur)
- [GitHub Issues](https://github.com/zeabur/zeabur/issues)

---

**祝部署順利！** 🚀
