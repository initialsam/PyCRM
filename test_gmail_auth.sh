#!/bin/bash

echo "=== Gmail API 授权状态检查 ==="
echo ""

# 检查环境变量
echo "1. 检查环境变量:"
if [ -n "$GOOGLE_CLIENT_ID" ]; then
    echo "   ✓ GOOGLE_CLIENT_ID 已设置"
else
    echo "   ✗ GOOGLE_CLIENT_ID 未设置"
fi

if [ -n "$GOOGLE_CLIENT_SECRET" ]; then
    echo "   ✓ GOOGLE_CLIENT_SECRET 已设置"
else
    echo "   ✗ GOOGLE_CLIENT_SECRET 未设置"
fi

if [ -n "$OAUTH_REDIRECT_URI" ]; then
    echo "   ✓ OAUTH_REDIRECT_URI: $OAUTH_REDIRECT_URI"
else
    echo "   ⚠ OAUTH_REDIRECT_URI 未设置 (将使用默认值)"
fi

echo ""

# 检查 token 文件
echo "2. 检查 Token 文件:"
if [ -f "gmail_token.pickle" ]; then
    echo "   ✓ gmail_token.pickle 存在"
    ls -lh gmail_token.pickle
else
    echo "   ✗ gmail_token.pickle 不存在"
fi

echo ""
echo "=== 修复说明 ==="
echo ""
echo "已修复 is_authenticated() 方法的问题："
echo "• 现在会自动刷新过期的 token"
echo "• 不再因为 token 过期而显示需要授权"
echo ""
echo "如果仍然出现授权问题，请尝试："
echo "1. 重新启动应用"
echo "2. 清除 gmail_token.pickle 并重新授权"
echo "3. 确认 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET 正确"
