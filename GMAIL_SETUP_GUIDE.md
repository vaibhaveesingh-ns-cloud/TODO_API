# Gmail Email Verification Setup Guide

## Step 1: Enable 2-Factor Authentication

1. **Go to your Google Account**: https://myaccount.google.com/
2. **Click "Security"** in the left sidebar
3. **Find "2-Step Verification"** and click it
4. **Follow the setup process** if not already enabled
5. **Verify it's enabled** - you should see "2-Step Verification: On"

## Step 2: Generate App Password

1. **Go back to Security settings**: https://myaccount.google.com/security
2. **Click "2-Step Verification"**
3. **Scroll down and click "App passwords"**
4. **Select "Mail" from the dropdown**
5. **Click "Generate"**
6. **Copy the 16-character password** (format: xxxx xxxx xxxx xxxx)
7. **Save this password** - you won't see it again!

## Step 3: Configure Environment Variables

Choose one of these methods:

### Method A: Terminal Environment Variables (Temporary)
```bash
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-16-char-app-password"
export FROM_EMAIL="your-email@gmail.com"
export EMAIL_SECRET_KEY="your-secure-secret-key-change-me"
```

### Method B: Create .env File (Recommended)
```bash
# Create .env file in project root
cd /Users/vaibhavee/project/TODO_fastapi
touch .env
```

Add this content to `.env`:
```
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
FROM_EMAIL=your-email@gmail.com
EMAIL_SECRET_KEY=your-secure-secret-key-change-me
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FRONTEND_URL=http://localhost:3000
```

## Step 4: Update run_local.py to Load .env

The system needs to load environment variables from .env file.

## Step 5: Test the Setup

1. **Restart your backend server**
2. **Register a new user**
3. **Check your email inbox** (and spam folder)
4. **Click the verification link**

## Example Configuration

Replace these values with your actual Gmail credentials:

```
SMTP_USERNAME=john.doe@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=john.doe@gmail.com
EMAIL_SECRET_KEY=my-super-secret-key-for-email-tokens
```

## Security Notes

- ⚠️ **Never commit .env file to git** (it's already in .gitignore)
- 🔒 **Use App Password, not your regular Gmail password**
- 🔑 **Change EMAIL_SECRET_KEY from default value**
- 📧 **The FROM_EMAIL should match SMTP_USERNAME**

## Troubleshooting

### "Authentication failed"
- Make sure you're using the App Password, not regular password
- Verify 2FA is enabled on your Gmail account
- Check that username/password are correct

### "Connection refused"
- Check internet connection
- Verify SMTP server (smtp.gmail.com) and port (587)

### "Email not received"
- Check spam/junk folder
- Verify email address is correct
- Check backend console for error messages

### "App passwords not available"
- 2-Factor Authentication must be enabled first
- Some Google Workspace accounts may have restrictions
