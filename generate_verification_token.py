#!/usr/bin/env python3
"""
Generate email verification tokens for testing purposes
"""

from itsdangerous import URLSafeTimedSerializer

# Same secret as in email_utils.py
SECRET = "EMAIL_CHANGE_ME"
s = URLSafeTimedSerializer(SECRET)

def generate_token_for_email(email: str):
    """Generate verification token for given email"""
    token = s.dumps(email, salt="email-confirm")
    return token

def verify_token(token: str):
    """Verify and decode a token"""
    try:
        email = s.loads(token, salt="email-confirm", max_age=3600)
        return email
    except Exception as e:
        return f"Invalid token: {e}"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Generate token: python generate_verification_token.py generate test@example.com")
        print("  Verify token:   python generate_verification_token.py verify TOKEN_HERE")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "generate" and len(sys.argv) >= 3:
        email = sys.argv[2]
        token = generate_token_for_email(email)
        print(f"Email: {email}")
        print(f"Token: {token}")
        print(f"Verification URL: http://localhost:8000/auth/verify-email?token={token}")
    
    elif action == "verify" and len(sys.argv) >= 3:
        token = sys.argv[2]
        result = verify_token(token)
        print(f"Token verification result: {result}")
    
    else:
        print("Invalid arguments. Use 'generate EMAIL' or 'verify TOKEN'")
