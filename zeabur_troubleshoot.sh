#!/bin/bash
echo "========================================="
echo "🔍 Zeabur 部署問題診斷"
echo "========================================="
echo ""

echo "請選擇你遇到的問題："
echo ""
echo "1) 構建失敗 (Build Failed)"
echo "2) 應用無法啟動 (Application won't start)"
echo "3) 資料庫連線錯誤 (Database connection error)"
echo "4) 404 錯誤 (404 errors)"
echo "5) 靜態檔案無法載入 (Static files not loading)"
echo "6) 環境變數問題 (Environment variables issue)"
echo "7) 顯示所有檢查項目"
echo ""
read -p "請輸入選項 (1-7): " choice

case $choice in
    1)
        echo ""
        echo "=== 構建失敗診斷 ==="
        echo ""
        echo "1. 檢查 requirements.txt："
        if [ -f "requirements.txt" ]; then
            echo "   ✅ requirements.txt 存在"
            echo "   套件數量: $(wc -l < requirements.txt)"
        else
            echo "   ❌ requirements.txt 不存在"
            echo "   解決: 執行 'uv pip freeze > requirements.txt'"
        fi
        echo ""
        echo "2. 檢查 Dockerfile："
        if [ -f "Dockerfile" ]; then
            echo "   ✅ Dockerfile 存在"
        else
            echo "   ❌ Dockerfile 不存在"
        fi
        echo ""
        echo "3. 常見原因："
        echo "   - 缺少系統依賴（如 gcc, postgresql-dev）"
        echo "   - requirements.txt 中的套件版本衝突"
        echo "   - Python 版本不相容"
        echo ""
        echo "解決方案："
        echo "   查看 Zeabur Build Logs 中的錯誤訊息"
        echo "   確認所有依賴都可正常安裝"
        ;;
    2)
        echo ""
        echo "=== 應用啟動失敗診斷 ==="
        echo ""
        echo "1. 檢查啟動命令："
        if [ -f "Procfile" ]; then
            echo "   ✅ Procfile: $(cat Procfile)"
        else
            echo "   ❌ Procfile 不存在"
        fi
        echo ""
        echo "2. 檢查端口配置："
        if grep -q "PORT" app/main.py; then
            echo "   ✅ main.py 支援動態端口"
        else
            echo "   ❌ main.py 未支援動態端口"
            echo "   需要修改: port = int(os.getenv('PORT', 8000))"
        fi
        echo ""
        echo "3. 檢查應用入口："
        if [ -f "app/main.py" ]; then
            echo "   ✅ app/main.py 存在"
        else
            echo "   ❌ 找不到 app/main.py"
        fi
        ;;
    3)
        echo ""
        echo "=== 資料庫連線診斷 ==="
        echo ""
        echo "1. 檢查資料庫配置："
        if grep -q "POSTGRES_URL" app/database.py; then
            echo "   ✅ 支援 POSTGRES_URL 環境變數"
        else
            echo "   ⚠️  建議添加 POSTGRES_URL 支援"
        fi
        echo ""
        echo "2. Zeabur 環境變數設定："
        echo "   在 Zeabur Dashboard 設定："
        echo "   DATABASE_URL = \${POSTGRES_URL}"
        echo ""
        echo "3. 連線字串格式："
        echo "   postgresql://user:password@host:port/database"
        echo ""
        echo "4. 常見問題："
        echo "   - PostgreSQL 服務未啟動"
        echo "   - 環境變數未設定"
        echo "   - 連線字串格式錯誤"
        ;;
    4)
        echo ""
        echo "=== 404 錯誤診斷 ==="
        echo ""
        echo "檢查路由設定："
        echo "   /              → Dashboard"
        echo "   /dashboard     → 主頁面"
        echo "   /docs          → API 文件"
        echo "   /api/clients/  → API 端點"
        echo ""
        echo "如果特定路徑 404："
        echo "   1. 檢查 app/main.py 中的路由定義"
        echo "   2. 確認 templates/ 和 static/ 目錄已推送"
        echo "   3. 查看 Zeabur Runtime Logs"
        ;;
    5)
        echo ""
        echo "=== 靜態檔案診斷 ==="
        echo ""
        if [ -d "app/static" ]; then
            echo "   ✅ app/static 目錄存在"
            echo "   檔案: $(find app/static -type f | wc -l) 個"
        else
            echo "   ❌ app/static 目錄不存在"
        fi
        echo ""
        if [ -d "app/templates" ]; then
            echo "   ✅ app/templates 目錄存在"
            echo "   檔案: $(find app/templates -type f | wc -l) 個"
        else
            echo "   ❌ app/templates 目錄不存在"
        fi
        echo ""
        echo "檢查 main.py 中的靜態檔案掛載："
        if grep -q "StaticFiles" app/main.py; then
            echo "   ✅ 靜態檔案已掛載"
        else
            echo "   ❌ 未掛載靜態檔案"
        fi
        ;;
    6)
        echo ""
        echo "=== 環境變數診斷 ==="
        echo ""
        echo "必要的環境變數："
        echo "   DATABASE_URL 或 POSTGRES_URL"
        echo ""
        echo "可選的環境變數："
        echo "   PORT (Zeabur 自動注入)"
        echo ""
        echo "在 Zeabur 設定方法："
        echo "   1. 進入應用服務頁面"
        echo "   2. 點擊 'Variables' 標籤"
        echo "   3. 添加環境變數"
        echo "   4. 儲存並重新部署"
        ;;
    7)
        echo ""
        echo "=== 完整檢查 ==="
        ./deploy_check.sh
        ;;
    *)
        echo "無效選項"
        ;;
esac

echo ""
echo "========================================="
echo "📚 更多資源"
echo "========================================="
echo ""
echo "文件："
echo "   - 完整部署指南: cat ZEABUR_DEPLOY.md"
echo "   - 快速開始: cat DEPLOY_QUICK_START.md"
echo ""
echo "Zeabur 資源："
echo "   - 文件: https://zeabur.com/docs"
echo "   - Discord: https://discord.gg/zeabur"
echo ""
