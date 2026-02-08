# 📧 郵件模板初始化 - 正確版本

## 方法 1: 單行版本（最簡單）

在瀏覽器 Console 貼上這一行：

```javascript
fetch('/api/templates/init', {method: 'POST'}).then(r => r.json()).then(d => alert('完成: ' + JSON.stringify(d)));
```

---

## 方法 2: 完整版本（有提示）

```javascript
fetch('/api/templates/init', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
}).then(function(response) {
  return response.json();
}).then(function(data) {
  console.log(data);
  alert('模板已建立！請刷新頁面 (F5)');
}).catch(function(error) {
  console.error(error);
  alert('失敗: ' + error);
});
```

---

## 方法 3: 使用 jQuery（如果網頁有載入 jQuery）

```javascript
$.post('/api/templates/init', function(data) {
  alert('模板已建立：' + JSON.stringify(data));
  location.reload();
});
```

---

## 方法 4: 直接訪問 URL（最可靠）

**不使用 Console，直接在瀏覽器訪問：**

```
https://pycrm.zeabur.app/api/templates/init
```

但這只能用 GET 方法，我們需要修改路由。

---

## 方法 5: 使用 curl（命令行）

如果你有訪問伺服器的權限：

```bash
curl -X POST https://pycrm.zeabur.app/api/templates/init \
  -H "Cookie: session=你的session_cookie"
```

---

## 推薦：使用單行版本

**直接複製這一行到 Console：**

```
fetch('/api/templates/init',{method:'POST'}).then(r=>r.json()).then(d=>alert('完成!請按F5刷新'))
```

執行後：
1. 看到「完成!請按F5刷新」提示
2. 按 F5 刷新頁面
3. 前往 `/send-email` 確認模板

---

## 如果還是報錯

### 錯誤 1: "Uncaught SyntaxError"
**原因**: 複製時包含了特殊字符
**解決**: 手動輸入，或使用單行版本

### 錯誤 2: "401 Unauthorized"
**原因**: 未登入
**解決**: 先訪問 `/login` 登入

### 錯誤 3: "模板已存在"
**原因**: 已經初始化過了
**解決**: 
```javascript
fetch('/api/templates').then(r=>r.json()).then(d=>console.log('模板數量:', d.length))
```

檢查是否已有模板。

---

## 最簡單的驗證方法

在 Console 執行：

```javascript
fetch('/api/templates').then(r=>r.json()).then(d=>console.table(d))
```

這會顯示所有模板的表格。如果有 3 個模板，就成功了！
