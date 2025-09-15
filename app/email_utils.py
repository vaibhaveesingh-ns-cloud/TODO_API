from itsdangerous import URLSafeTimedSerializer

# For demo only. In prod use a proper mail service and secure secret.
SECRET = "EMAIL_CHANGE_ME"
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
    # MOCK: in dev, print to console. In prod, integrate with SMTP or SendGrid.
    verification_link = f"http://127.0.0.1:8000/auth/verify-email?token={token}"
    print(f"MOCK EMAIL -> to: {email}\nClick: {verification_link}")
