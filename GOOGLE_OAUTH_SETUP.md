# Google OAuth 2.0 Setup Guide

This guide explains how to set up Google OAuth 2.0 authentication for IQAutoJobs.

## Prerequisites

- Google Cloud Platform account
- Access to Google Cloud Console

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API or Google Identity Services

## Step 2: Configure OAuth Consent Screen

1. In the Google Cloud Console, navigate to **APIs & Services** > **OAuth consent screen**
2. Select **External** user type (or Internal if using Google Workspace)
3. Fill in the required information:
   - App name: `IQAutoJobs`
   - User support email: Your email
   - Developer contact email: Your email
4. Add scopes:
   - `openid`
   - `email`
   - `profile`
5. Save and continue

## Step 3: Create OAuth 2.0 Client ID

1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth 2.0 Client ID**
3. Select **Web application** as the application type
4. Configure the OAuth client:
   - **Name**: `IQAutoJobs Web Client`
   - **Authorized JavaScript origins**: 
     - `https://9eb1f130-da4c-4609-95eb-77a71d11ad99-00-29kyt26ktfkbx.pike.replit.dev`
     - (Replace with your actual Replit dev domain)
   - **Authorized redirect URIs**:
     - `https://9eb1f130-da4c-4609-95eb-77a71d11ad99-00-29kyt26ktfkbx.pike.replit.dev/api/oauth/google/callback`
     - (Replace with your actual Replit dev domain)
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

## Step 4: Configure Environment Variables

Add the following environment variables to your project:

### Backend Environment Variables (.env or Replit Secrets)

```bash
# Google OAuth Configuration
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
GOOGLE_OAUTH_REDIRECT_URI=https://9eb1f130-da4c-4609-95eb-77a71d11ad99-00-29kyt26ktfkbx.pike.replit.dev/api/oauth/google/callback
```

**Important**: Replace `9eb1f130-da4c-4609-95eb-77a71d11ad99-00-29kyt26ktfkbx.pike.replit.dev` with your actual Replit dev domain.

## Step 5: Restart Backend Server

After setting the environment variables, restart the backend server for the changes to take effect:

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## How It Works

1. **User clicks "Continue with Google"** on the login or register page
2. **Redirect to Google** for authentication
3. **Google callback** returns authorization code
4. **Backend exchanges code** for access token and user info
5. **Create or login user**:
   - If user with Google ID exists, log them in
   - If user with email exists, link Google OAuth to their account
   - If new user, create account with Google email and name
6. **Return JWT tokens** via httpOnly cookies
7. **Redirect user** to dashboard or returnTo URL

## Features

- ✅ New user registration via Google
- ✅ Existing user login via Google
- ✅ Link Google OAuth to existing email accounts
- ✅ Same JWT token flow as email/password auth
- ✅ Secure httpOnly cookies for token storage
- ✅ CSRF protection with state parameter
- ✅ Support for returnTo parameter for deep linking

## Security Considerations

- OAuth state parameter prevents CSRF attacks
- Tokens stored in httpOnly cookies (not accessible via JavaScript)
- OAuth users don't have passwords (password_hash is NULL)
- Users can login with either email/password OR Google OAuth
- Audit logs track OAuth registration and login events

## Troubleshooting

### "Google OAuth is not configured" error

Make sure all three environment variables are set:
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GOOGLE_OAUTH_REDIRECT_URI`

### "Redirect URI mismatch" error

Ensure the redirect URI in Google Cloud Console exactly matches:
```
https://YOUR_REPLIT_DEV_DOMAIN/api/oauth/google/callback
```

### "Invalid state parameter" error

This can happen if:
- The backend server restarted between OAuth initiation and callback
- The state expired (currently stored in memory)
- Consider using Redis for production state storage

## Database Changes

The following database changes were made to support OAuth:

```sql
ALTER TABLE users 
ADD COLUMN oauth_provider VARCHAR(50),
ADD COLUMN oauth_id VARCHAR(255);

ALTER TABLE users 
ALTER COLUMN password_hash DROP NOT NULL;
```

Users created via OAuth will have:
- `oauth_provider` = `"google"`
- `oauth_id` = Google user ID
- `password_hash` = `NULL`

## API Endpoints

### Backend (FastAPI)

- `GET /api/oauth/google/login?returnTo=/dashboard` - Initiates OAuth flow
- `GET /api/oauth/google/callback?code=...&state=...` - Handles OAuth callback

### Frontend (Next.js)

- `GET /api/oauth/google/login?returnTo=/dashboard` - Proxy to backend, redirects to Google
- `GET /api/oauth/callback?access_token=...&refresh_token=...&returnTo=...` - Sets cookies and redirects

## Testing

1. Click "Continue with Google" on the login page
2. Select a Google account
3. Grant permissions
4. You should be redirected back and logged in
5. Check that your user appears in the database with `oauth_provider='google'`

## Production Deployment

For production:

1. Update OAuth consent screen to production mode
2. Add production domain to authorized origins and redirect URIs
3. Use Redis or similar for state storage instead of in-memory
4. Set `secure: true` for cookies (HTTPS only)
5. Consider rate limiting OAuth endpoints
6. Monitor audit logs for suspicious OAuth activity
