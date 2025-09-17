import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer

# Email configuration from environment variables
SECRET = os.getenv("EMAIL_SECRET_KEY", "EMAIL_CHANGE_ME")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

s = URLSafeTimedSerializer(SECRET)

def generate_verification_token(email: str):
    return s.dumps(email, salt="email-confirm")

def confirm_verification_token(token: str, expires_sec=3600):
    try:
        email = s.loads(token, salt="email-confirm", max_age=expires_sec)
    except Exception:
        return None
    return email

def send_verification_email(email: str, token: str):
    """Send verification email to user"""
    verification_link = f"{FRONTEND_URL}/verify-email?token={token}"
    
    # If SMTP credentials are not configured, fall back to console logging
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print(f"\n{'='*60}")
        print(f"📧 EMAIL VERIFICATION REQUIRED")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Subject: Verify your email address")
        print(f"Verification Link: {verification_link}")
        print(f"{'='*60}")
        print(f"⚠️  SMTP not configured - email printed to console")
        print(f"   Configure SMTP_USERNAME and SMTP_PASSWORD to send real emails")
        print(f"{'='*60}\n")
        return
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = "Verify your email address - TaskMaster"
        
        # Email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">📝 TaskMaster</h1>
                <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 16px;">Welcome to your productivity journey!</p>
            </div>
            
            <div style="background: #ffffff; padding: 40px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #333; margin-top: 0;">Verify Your Email Address</h2>
                
                <p>Hi there! 👋</p>
                
                <p>Thank you for signing up for TaskMaster! To complete your registration and start managing your todos, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 8px; 
                              font-weight: bold; 
                              font-size: 16px;
                              display: inline-block;
                              transition: transform 0.2s;">
                        ✅ Verify Email Address
                    </a>
                </div>
                
                <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                <p style="background: #f8f9fa; padding: 15px; border-radius: 5px; word-break: break-all; font-family: monospace; font-size: 14px;">
                    {verification_link}
                </p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="font-size: 14px; color: #666;">
                        <strong>Security Note:</strong> This verification link will expire in 1 hour for your security.
                    </p>
                    <p style="font-size: 14px; color: #666;">
                        If you didn't create an account with TaskMaster, you can safely ignore this email.
                    </p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #666; font-size: 12px;">
                <p>© 2024 TaskMaster. Made with ❤️ for productivity.</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, email, text)
        server.quit()
        
        print(f"✅ Verification email sent successfully to {email}")
        
    except Exception as e:
        print(f"❌ Failed to send verification email to {email}: {str(e)}")
        # Fall back to console logging
        print(f"\n📧 FALLBACK - Verification link: {verification_link}\n")
