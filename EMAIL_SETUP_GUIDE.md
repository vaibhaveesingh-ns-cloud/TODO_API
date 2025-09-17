# Email Verification Setup Guide

## Current Issue
Your TODO application is not sending verification emails because the email system is using a mock implementation. Here's how to fix it:

## Quick Fix (Development)
**The verification links are printed to the console!** 

When you register a new user, check your terminal where the backend is running. You'll see output like:
```
============================================================
📧 EMAIL VERIFICATION REQUIRED
============================================================
To: user@example.com
Subject: Verify your email address
Verification Link: http://localhost:3000/verify-email?token=...
============================================================
⚠️  SMTP not configured - email printed to console
   Configure SMTP_USERNAME and SMTP_PASSWORD to send real emails
============================================================
```

Copy the verification link and paste it in your browser to verify the email.

## Permanent Fix (Real Email Sending)

### Option 1: Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Copy the 16-character password

3. **Set Environment Variables:**
   ```bash
   export SMTP_USERNAME="your-email@gmail.com"
   export SMTP_PASSWORD="your-16-char-app-password"
   export FROM_EMAIL="your-email@gmail.com"
   export EMAIL_SECRET_KEY="your-secret-key-change-me"
   ```

4. **Restart your backend server**

### Option 2: Other Email Providers

**Outlook/Hotmail:**
```bash
export SMTP_SERVER="smtp.office365.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@outlook.com"
export SMTP_PASSWORD="your-password"
```

**Yahoo:**
```bash
export SMTP_SERVER="smtp.mail.yahoo.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@yahoo.com"
export SMTP_PASSWORD="your-app-password"
```

### Option 3: Using .env File

1. Create `.env` file in project root:
   ```bash
   touch .env
   ```

2. Add configuration:
   ```
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   EMAIL_SECRET_KEY=your-secret-key-change-me
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   FRONTEND_URL=http://localhost:3000
   ```

3. Install python-dotenv (already in requirements.txt)

4. Update your startup script to load .env file

## Testing Email Setup

1. **Register a new user** through the frontend
2. **Check console output** - should show "✅ Verification email sent successfully"
3. **Check your email** for the verification message
4. **Click the verification link** or copy it to your browser

## Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Make sure you're using an App Password, not your regular password
   - Check that 2FA is enabled on your Gmail account

2. **"Connection refused"**
   - Check your internet connection
   - Verify SMTP server and port settings

3. **"Email not received"**
   - Check spam/junk folder
   - Verify the email address is correct
   - Check console for error messages

### Development Workaround

If you can't set up email immediately, you can manually activate users:

```python
# Run this in your Python environment
from app.database import SessionLocal
from app import crud

db = SessionLocal()
user = crud.get_user_by_email(db, "user@example.com")
if user:
    crud.activate_user(db, user)
    print(f"User {user.username} activated!")
db.close()
```

Or use the existing `debug_auth.py` script:
```bash
python debug_auth.py
```

## Security Notes

- Never commit real email credentials to version control
- Use environment variables or secure secret management
- Change the EMAIL_SECRET_KEY from the default value
- Consider using services like SendGrid or AWS SES for production

## Email Template

The system now sends beautiful HTML emails with:
- Professional TaskMaster branding
- Clear call-to-action button
- Fallback text link
- Security information
- Responsive design

Once configured, users will receive properly formatted verification emails instead of console output.
