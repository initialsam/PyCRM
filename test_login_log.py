#!/usr/bin/env python3
"""
測試登入日志功能
"""
import os
import sys

# 設定測試環境變數
os.environ['ALLOWED_EMAILS'] = 'helpaction4u@gmail.com,test@example.com'

# 導入模組
from app.auth import is_email_allowed, get_allowed_emails

print("=" * 60)
print("測試 ALLOWED_EMAILS 白名單與日志功能")
print("=" * 60)

print("\n1. 顯示白名單內容：")
allowed = get_allowed_emails()
print(f"   {allowed}")

print("\n2. 測試白名單內的 email (應該通過)：")
result1 = is_email_allowed("helpaction4u@gmail.com")
print(f"   結果: {result1}")

print("\n3. 測試白名單內的 email 大小寫不同 (應該通過)：")
result2 = is_email_allowed("HELPACTION4U@GMAIL.COM")
print(f"   結果: {result2}")

print("\n4. 測試不在白名單的 email (應該失敗)：")
result3 = is_email_allowed("notallowed@gmail.com")
print(f"   結果: {result3}")

print("\n5. 測試白名單內的第二個 email (應該通過)：")
result4 = is_email_allowed("test@example.com")
print(f"   結果: {result4}")

print("\n6. 測試空 email (應該失敗)：")
result5 = is_email_allowed("")
print(f"   結果: {result5}")

print("\n" + "=" * 60)
print("測試完成！請檢查上方的日志輸出")
print("=" * 60)
