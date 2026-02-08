# 🚀 Zeabur 快速部署指令

## 📦 準備階段（已完成）

所有必要檔案已建立：
- ✅ requirements.txt
- ✅ Dockerfile  
- ✅ Procfile
- ✅ zeabur.json
- ✅ .env.example
- ✅ .gitignore

## 🔍 部署前檢查

```bash
./deploy_check.sh
```

## 📤 部署到 Zeabur

### 步驟 1：推送到 GitHub

```bash
# 初始化 Git（如果需要）
git init

# 添加所有檔案
git add .

# 提交
git commit -m "Ready for Zeabur deployment"

# 連接到你的 GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 推送
git push -u origin main
```

### 步驟 2：Zeabur 控制台設定

1. **訪問 Zeabur Dashboard**
   - https://dash.zeabur.com

2. **建立新專案**
   - 點擊 "Create Project"
   - 輸入專案名稱（例如：crm-system）

3. **添加 PostgreSQL 服務**
   ```
   點擊 "Add Service" → 選擇 "PostgreSQL"
   ```

4. **添加應用服務**
   ```
   點擊 "Add Service" → 選擇 "Git"
   → 選擇你的 GitHub repository
   ```

5. **設定環境變數**
   在應用服務的 "Variables" 頁面設定：
   ```
   DATABASE_URL = ${POSTGRES_URL}
   ```

### 步驟 3：等待部署完成

Zeabur 會自動：
- 偵測 Dockerfile
- 構建 Docker 映像
- 部署應用
- 分配域名

### 步驟 4：訪問應用

部署完成後，點擊應用名稱旁的網址圖標，或訪問：
```
https://your-app-name.zeabur.app
```

## 🎯 重要端點

部署成功後測試：

```bash
# API 文件
https://your-app.zeabur.app/docs

# Dashboard
https://your-app.zeabur.app/dashboard

# 統計 API
https://your-app.zeabur.app/api/clients/statistics
```

## 🔧 環境變數設定

### 必要變數

**DATABASE_URL**
```
方法 1（推薦）：使用 Zeabur PostgreSQL
${POSTGRES_URL}

方法 2：手動設定
postgresql://username:password@host:port/database
```

### 可選變數

**PORT**（Zeabur 會自動注入，通常不需設定）

## 🐛 常見問題

### Q1: 構建失敗
**檢查**：
```bash
# 確認 requirements.txt 正確
cat requirements.txt

# 查看 Zeabur Build Logs
```

### Q2: 應用無法啟動
**解決**：
- 檢查 Zeabur Runtime Logs
- 確認 DATABASE_URL 已設定
- 驗證 PostgreSQL 服務運行正常

### Q3: 資料庫連線錯誤
**解決**：
```
1. 確認 PostgreSQL 服務已添加並啟動
2. 檢查環境變數：DATABASE_URL = ${POSTGRES_URL}
3. 查看應用 Logs 中的錯誤訊息
```

### Q4: 靜態檔案 404
**解決**：
- 確認 `app/static` 目錄已推送到 Git
- 檢查 `app/main.py` 中的靜態檔案掛載

### Q5: 如何查看資料庫
**方法**：
1. 在 Zeabur PostgreSQL 服務頁面
2. 點擊 "Instructions"  
3. 使用提供的連線資訊
4. 或點擊 "Connect" 直接打開 Web Terminal

## 🔄 更新部署

### 自動部署（GitHub 連接）
```bash
git add .
git commit -m "Update feature"
git push
```
Zeabur 會自動偵測並重新部署

### 手動觸發
在 Zeabur Dashboard 中點擊 "Redeploy"

## 📊 監控和日誌

### 查看日誌
```
Zeabur Dashboard → 選擇你的服務 → Logs 標籤
```

### 監控指標
```
Zeabur Dashboard → 選擇你的服務 → Metrics 標籤
```

## ✅ 部署檢查清單

部署前確認：
- [ ] 程式碼已提交到 Git
- [ ] 已推送到 GitHub
- [ ] Zeabur 專案已建立
- [ ] PostgreSQL 服務已添加
- [ ] 應用服務已連接 GitHub
- [ ] 環境變數已設定
- [ ] 應用已成功啟動

部署後驗證：
- [ ] 可以訪問 Dashboard
- [ ] API 文件正常顯示
- [ ] 統計資料正確顯示
- [ ] 可以新增客戶
- [ ] 可以匯入 CSV

## 🎉 部署成功

恭喜！你的 CRM 系統已成功部署到 Zeabur！

你的應用網址：
```
https://your-app-name.zeabur.app
```

---

**需要更多幫助？**
- 查看完整指南：`cat ZEABUR_DEPLOY.md`
- Zeabur 文件：https://zeabur.com/docs
- 問題回報：在 Zeabur Discord 尋求協助
