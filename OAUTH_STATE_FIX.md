# OAuth State Mismatch Fix

## Problem
```
MismatchingStateError: mismatching_state: CSRF Warning! State not equal in request and response.
```

## Root Cause
The SessionMiddleware was using default cookie settings without explicit configuration. This caused:
1. Session cookies not persisting properly between OAuth redirect and callback
2. The CSRF state token stored in session was lost before the callback could verify it

## Solution Applied

### 1. Explicit Session Configuration
Added explicit cookie settings in `app/main.py`:
```python
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    session_cookie="session",
    max_age=3600,  # 1 hour
    same_site="lax",  # 允許跨站點但限制，適合 OAuth
    https_only=False  # 在開發環境設為 False
)
```

### 2. Enhanced Logging
Added detailed logging to track:
- OAuth flow initialization with redirect URI
- Session ID at each step
- Callback URL and session state

## Key Parameters

- **same_site="lax"**: Allows cookies to be sent with top-level navigation (needed for OAuth callbacks)
- **max_age=3600**: Ensures session persists long enough for OAuth flow
- **https_only=False**: Set to False for dev, should be True in production with HTTPS

## Production Deployment

For production (Zeabur), ensure:
1. Set `SECRET_KEY` environment variable to a strong random value
2. Consider setting `https_only=True` if using HTTPS
3. Monitor logs for session ID consistency between auth/login and auth/callback

## Testing
1. Clear browser cookies
2. Navigate to `/login`
3. Click "Login with Google"
4. Complete OAuth flow
5. Should redirect to `/dashboard` successfully
