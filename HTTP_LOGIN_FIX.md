# HTTP 登入支援測試

## 問題說明

之前的程式碼會自動將 HTTP 改為 HTTPS：

```python
# 舊版本（有問題）
if not os.getenv('OAUTH_REDIRECT_URI') and request.url.scheme == 'http':
    redirect_uri = redirect_uri.replace('http://', 'https://')
```

這會導致：
- 本地開發使用 http://localhost:8000
- 但 redirect_uri 被改為 https://localhost:8000/auth/callback
- Google OAuth 回調失敗（redirect_uri_mismatch）

## 修正方案

```python
# 新版本（已修正）
redirect_uri = os.getenv('OAUTH_REDIRECT_URI')
if not redirect_uri:
    redirect_uri = str(request.url_for('auth_callback'))
    # 保持原始 scheme（http 或 https）
```

## Google Cloud Console 設定

確保在「已授權的重新導向 URI」中同時新增：

### 本地開發（HTTP）
```
http://localhost:8000/auth/callback
http://localhost:8000/auth/gmail/callback
```

### 生產環境（HTTPS）
```
https://your-domain.com/auth/callback
https://your-domain.com/auth/gmail/callback
```

## 測試步驟

1. 啟動本地開發伺服器：
   ```bash
   uvicorn app.main:app --reload
   ```

2. 訪問 http://localhost:8000/login

3. 點擊「使用 Google 帳號登入」

4. 應該成功重新導向到 Google 授權頁面

5. 授權後應該成功回調到 http://localhost:8000/auth/callback

## 環境變數設定

### 本地開發
```env
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
```

### 生產環境（Zeabur）
```env
OAUTH_REDIRECT_URI=https://your-domain.zeabur.app/auth/callback
```

### 自動偵測（不設定）
如果不設定 `OAUTH_REDIRECT_URI`，系統會自動使用當前請求的 scheme：
- HTTP 請求 → http://localhost:8000/auth/callback
- HTTPS 請求 → https://your-domain.com/auth/callback

## 注意事項

1. ✅ HTTP 和 HTTPS 都支援
2. ✅ 本地開發可以使用 HTTP
3. ✅ 生產環境建議使用 HTTPS
4. ⚠️ Google OAuth 需要在 Console 中同時設定 HTTP 和 HTTPS URI
5. ⚠️ 某些瀏覽器可能對 HTTP OAuth 有安全警告

## 已修正

- ✅ app/main.py - 移除強制 HTTPS 轉換
- ✅ 保持原始請求的 scheme
- ✅ 支援 HTTP 本地開發
- ✅ 支援 HTTPS 生產環境
