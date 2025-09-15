#!/usr/bin/env python3
"""
Generate verification tokens for existing users
"""
from app.database import SessionLocal
from app.models import User
from app import email_utils

def generate_token_for_user(username: str):
    """Generate verification token for a specific user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found!")
            return None
        
        # Generate verification token
        token = email_utils.generate_verification_token(user.email)
        verification_link = f"http://127.0.0.1:8000/auth/verify-email?token={token}"
        
        print(f"=== Verification Token for {username} ===")
        print(f"Email: {user.email}")
        print(f"Token: {token}")
        print(f"Full URL: {verification_link}")
        print(f"Status: {'Already Active' if user.is_active else 'Needs Verification'}")
        
        return token
    finally:
        db.close()

def list_users_and_generate_tokens():
    """List all users and generate tokens for inactive ones"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("=== All Users and Their Verification Links ===\n")
        
        for user in users:
            token = email_utils.generate_verification_token(user.email)
            verification_link = f"http://127.0.0.1:8000/auth/verify-email?token={token}"
            
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Active: {user.is_active}")
            print(f"Verification URL: {verification_link}")
            print("-" * 60)
        
        return users
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Email Verification Token Generator ===\n")
    
    # List all users and their tokens
    users = list_users_and_generate_tokens()
    
    if users:
        print(f"\n=== Instructions ===")
        print("1. Copy any verification URL above")
        print("2. Paste it in your browser or Postman (GET request)")
        print("3. The user will be activated after successful verification")
        print("4. You can then use the activated user to login and get access tokens")
    else:
        print("No users found. Register a user first using POST /auth/register")
