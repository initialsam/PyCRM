# CRM 專案管理系統

使用 FastAPI + PostgreSQL + Pure CSS 建立的專案管理 CRM 系統。

## 功能特色

- 📊 Dashboard 管理介面
- 👥 客戶資料 CRUD 操作
- 📈 專案統計資訊
- 📁 CSV 檔案匯入
- 🔍 客戶搜尋功能
- 🔒 **Email 遮罩保護**（新功能）
- 📅 **智能排序**（按最後修改時間）
- 🔐 **Google OAuth 登入**（新功能）
- 🔒 **Email 白名單**（帳號權限控制）
- 📧 **Gmail API 郵件發送**（批量發送客製化郵件）
- 📱 響應式設計（Pure CSS）

## 技術棧

- **後端**: FastAPI
- **資料庫**: PostgreSQL
- **ORM**: SQLAlchemy
- **前端**: Jinja2 Templates + Pure CSS
- **套件管理**: uv

## 安裝步驟

### 1. 確認 PostgreSQL 已安裝並啟動

```bash
# 建立資料庫
createdb crm_db

# 或使用 psql
psql -U postgres
CREATE DATABASE crm_db;
```

### 2. 設定環境變數

編輯 `.env` 檔案，設定資料庫連線和 Google OAuth：

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crm_db
GOOGLE_CLIENT_ID=你的-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=你的-google-client-secret
SECRET_KEY=使用-openssl-rand-hex-32-生成的密鑰
ALLOWED_EMAILS=helpaction4u@gmail.com
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
```

**Google OAuth 設定**：請參閱 [GOOGLE_LOGIN_SETUP.md](GOOGLE_LOGIN_SETUP.md) 了解如何取得 Google OAuth 憑證。

**Email 白名單設定**：請參閱 [EMAIL_WHITELIST.md](EMAIL_WHITELIST.md) 了解如何設定允許登入的帳號。

**Gmail API 郵件發送**：請參閱 [EMAIL_SEND_GUIDE.md](EMAIL_SEND_GUIDE.md) 了解如何設定郵件發送功能。

### 3. 安裝相依套件

套件已透過 uv 管理，使用以下指令啟動：

```bash
uv run uvicorn app.main:app --reload
```

### 4. 啟動應用程式

```bash
# 開發模式（自動重載）
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或直接執行
uv run python app/main.py
```

應用程式將在 http://localhost:8000 啟動

## 使用說明

### 首次使用

1. 訪問 http://localhost:8000 會自動重導向到 Dashboard
2. 點擊「匯入 CSV」上傳 `client.csv` 檔案匯入資料
3. 在 Dashboard 查看客戶列表和統計資訊

### 主要功能

- **Dashboard**: 查看所有客戶資料和統計資訊
- **新增客戶**: 手動新增客戶資料
- **編輯客戶**: 修改現有客戶資訊（Email 預設鎖定保護）
- **刪除客戶**: 移除客戶資料（需確認）
- **搜尋**: 依客戶名稱或專案名稱搜尋
- **匯入 CSV**: 批次匯入客戶資料
- **Email 遮罩**: 保護客戶隱私，可選擇性顯示完整 Email
- **📧 發送郵件**: 批量發送客製化郵件給客戶
  - 使用 Gmail API 發送
  - 3 種預設模板（請款單、節日問候、促銷優惠）
  - 選擇客戶批量發送
  - 郵件預覽功能
- **📬 發送記錄**: 查看所有郵件發送歷史和狀態

### CSV 格式

CSV 檔案需包含以下欄位：

```
客戶名稱,專案名稱,email,專案費用
宏達數位,AI 智能客服系統,contact@honda-digital.com,250000
```

## API 文件

啟動後訪問：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 專案結構

```
CRM/
├── app/
│   ├── main.py              # FastAPI 主應用程式
│   ├── database.py          # 資料庫連接設定
│   ├── models.py            # SQLAlchemy 模型
│   ├── crud.py              # CRUD 操作
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Google OAuth 認證
│   ├── email_service.py     # Gmail API 郵件服務
│   ├── routers/
│   │   ├── clients.py       # 客戶相關 API
│   │   └── emails.py        # 郵件發送 API
│   ├── templates/           # Jinja2 模板
│   │   ├── send_email.html  # 郵件發送頁面
│   │   └── email_logs.html  # 發送記錄頁面
│   └── static/              # 靜態檔案（CSS/JS）
├── client.csv               # 範例資料
├── credentials.json         # Gmail API 憑證（需自行設定）
├── .env                     # 環境變數
└── pyproject.toml          # uv 專案設定
```

## 開發說明

### 修改資料庫模型

編輯 `app/models.py` 後需重啟應用程式，資料表會自動建立。

### 自訂樣式

編輯 `app/static/css/custom.css` 調整 UI 樣式。

## 授權

MIT License

---

## 🚀 部署到 Zeabur

本專案已準備好部署到 Zeabur 雲端平台！

### 快速開始
```bash
# 檢查部署準備
./deploy_check.sh

# 查看快速部署指南
cat DEPLOY_QUICK_START.md

# 問題診斷
./zeabur_troubleshoot.sh
```

### 部署檔案
- ✅ `Dockerfile` - Docker 容器配置
- ✅ `Procfile` - 啟動命令
- ✅ `requirements.txt` - Python 依賴
- ✅ `zeabur.json` - Zeabur 配置
- ✅ `.env.example` - 環境變數範例

### 詳細文件
- 📖 [完整部署指南](ZEABUR_DEPLOY.md)
- 🚀 [快速開始](DEPLOY_QUICK_START.md)

---

## 🆕 最新功能

### Email 遮罩保護
詳細說明請參閱：
- [功能說明](EMAIL_MASK_FEATURE.md)
- [使用演示](EMAIL_MASK_DEMO.md)

### 智能排序
客戶列表按最後修改時間自動排序（新→舊）
- [排序功能說明](SORT_FEATURE.md)

### Email 白名單系統
只有授權的 Email 才能登入系統
- [白名單設定說明](EMAIL_WHITELIST.md)

### 📧 Gmail API 郵件發送
批量發送客製化郵件給客戶
- [完整設定指南](EMAIL_SEND_GUIDE.md)
- 3 種預設模板：請款單、節日問候、促銷優惠
- 支援變數替換：客戶名稱、專案名稱、費用等
- 發送記錄追蹤
