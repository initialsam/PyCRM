# 🎯 CRM 專案管理系統 - 快速開始

## ✅ 系統已完成

您的 FastAPI + PostgreSQL + Pure CSS CRM 系統已經建置完成並正在運行！

## 🌐 訪問系統

**Dashboard (管理介面)**  
👉 http://localhost:8000

**API 文件 (Swagger UI)**  
👉 http://localhost:8000/docs

**ReDoc API 文件**  
👉 http://localhost:8000/redoc

## 📊 目前狀態

- ✅ 已匯入 10 筆客戶資料 (來自 client.csv)
- ✅ 總客戶數: 10
- ✅ 總專案金額: NT$ 2,500,000
- ✅ 平均專案金額: NT$ 250,000

## 🎨 主要功能

### 1️⃣ Dashboard 管理介面
- 📈 統計面板（總客戶數、總金額、平均金額）
- 📋 客戶列表（支援分頁）
- 🔍 搜尋功能（依客戶名稱或專案名稱）
- 📅 **智能排序**（最後修改時間優先）
- ✏️ 編輯客戶資料
- ❌ 刪除客戶（附確認機制）
- 🔒 Email 遮罩保護

### 2️⃣ 新增客戶
路徑: `/client/new`
- 客戶名稱
- 專案名稱
- Email
- 專案費用

### 3️⃣ CSV 匯入
路徑: `/import`
- 支援批次匯入客戶資料
- CSV 格式: `客戶名稱,專案名稱,email,專案費用`

## 🚀 啟動/管理指令

### 啟動系統
```bash
cd /mnt/n/vibe/CRM
./start.sh
```

### 手動啟動
```bash
cd /mnt/n/vibe/CRM
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 查看日誌
```bash
tail -f /tmp/fastapi-server.log
```

### 停止系統
```bash
pkill -f "uvicorn app.main:app"
```

### 測試系統
```bash
cd /mnt/n/vibe/CRM
./test_crm.sh
```

## 📁 專案結構

```
CRM/
├── app/
│   ├── main.py              # FastAPI 主應用
│   ├── database.py          # 資料庫連接
│   ├── models.py            # SQLAlchemy 模型
│   ├── schemas.py           # Pydantic 驗證
│   ├── crud.py              # CRUD 操作
│   ├── routers/
│   │   └── clients.py       # 客戶 API
│   ├── templates/           # Jinja2 模板
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── client_form.html
│   │   └── import_csv.html
│   └── static/
│       └── css/
│           └── custom.css   # 自訂樣式
├── client.csv               # 範例資料
├── .env                     # 環境變數
├── start.sh                 # 啟動腳本
├── test_crm.sh              # 測試腳本
└── README.md                # 完整文件
```

## 🔧 資料庫管理

### 連接資料庫
```bash
sudo -u postgres psql crm_db
```

### 查看客戶資料
```sql
SELECT * FROM clients;
```

### 清空資料
```sql
TRUNCATE TABLE clients RESTART IDENTITY;
```

### 重新匯入 CSV
訪問 http://localhost:8000/import 並上傳 `client.csv`

## 📡 API 端點

### 統計資訊
```bash
curl http://localhost:8000/api/clients/statistics
```

### 取得所有客戶
```bash
curl http://localhost:8000/api/clients/
```

### 搜尋客戶
```bash
curl "http://localhost:8000/api/clients/?search=關鍵字"
```

### 取得單一客戶
```bash
curl http://localhost:8000/api/clients/1
```

### 新增客戶
```bash
curl -X POST http://localhost:8000/api/clients/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "測試公司",
    "project_name": "測試專案",
    "email": "test@example.com",
    "project_cost": 100000
  }'
```

### 更新客戶
```bash
curl -X PUT http://localhost:8000/api/clients/1 \
  -H "Content-Type: application/json" \
  -d '{
    "project_cost": 300000
  }'
```

### 刪除客戶
```bash
curl -X DELETE http://localhost:8000/api/clients/1
```

### 匯入 CSV
```bash
curl -X POST -F "file=@client.csv" \
  http://localhost:8000/api/clients/import-csv
```

## 🎨 UI 設計

使用 [Pure CSS](https://pure-css.github.io/) 框架：
- 響應式設計（支援手機、平板、桌面）
- 簡潔現代的介面
- 藍色主題配色
- 自訂樣式位於 `app/static/css/custom.css`

## 🔐 資料庫設定

預設設定（可在 `.env` 修改）：
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crm_db
```

## 📝 注意事項

1. PostgreSQL 必須保持運行
2. 預設使用 port 8000
3. 開發模式會自動重載（修改程式碼後自動生效）
4. CSV 檔案必須是 UTF-8 編碼
5. 資料會持久保存在 PostgreSQL 中

## 🐛 疑難排解

### 無法連接資料庫
```bash
sudo systemctl start postgresql
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

### Port 已被占用
修改 `start.sh` 或手動指定其他 port：
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 查看錯誤日誌
```bash
tail -f /tmp/fastapi-server.log
```

## 🎉 完成！

您的 CRM 系統已經準備就緒！開始管理您的專案吧！

有任何問題歡迎查看 `README.md` 或 API 文件。
