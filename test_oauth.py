#!/usr/bin/env python3
"""測試 OAuth 設定"""

import os
from dotenv import load_dotenv

load_dotenv()

print("========================================")
print("  OAuth 設定檢查")
print("========================================")
print()

client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
redirect_uri = os.getenv('OAUTH_REDIRECT_URI')

print("1. GOOGLE_CLIENT_ID:")
if client_id:
    print(f"   ✅ {client_id[:50]}...")
else:
    print("   ❌ 未設定")

print()
print("2. GOOGLE_CLIENT_SECRET:")
if client_secret:
    print(f"   ✅ 已設定（長度：{len(client_secret)} 字元）")
else:
    print("   ❌ 未設定")

print()
print("3. OAUTH_REDIRECT_URI:")
if redirect_uri:
    print(f"   ✅ {redirect_uri}")
else:
    print("   ⚠️  未設定（將使用自動偵測）")

print()
print("========================================")
print("  Google Cloud Console 檢查")
print("========================================")
print()
print("請確認以下 URI 已加入「已授權的重新導向 URI」：")
print()
print(f"  □ {redirect_uri or 'http://localhost:8000/auth/callback'}")
print(f"  □ http://127.0.0.1:8000/auth/callback")
print()
print("========================================")
print("  測試授權 URL")
print("========================================")
print()

if client_id:
    from urllib.parse import urlencode
    
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri or 'http://localhost:8000/auth/callback',
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    print("完整授權 URL：")
    print(auth_url)
    print()
    print("可以手動訪問此 URL 測試 OAuth 流程")

print()
print("========================================")
