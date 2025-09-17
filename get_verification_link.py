#!/usr/bin/env python3
"""
Generate verification link for a specific email address
Usage: python get_verification_link.py user@example.com
"""
import sys
from app.database import SessionLocal
from app import email_utils, crud

def get_verification_link(email):
    """Generate and display verification link for an email"""
    db = SessionLocal()
    try:
        # Check if user exists
        user = crud.get_user_by_email(db, email)
        if not user:
            print(f"❌ User with email '{email}' not found!")
            return
        
        if user.is_active:
            print(f"✅ User '{user.username}' is already verified!")
            return
        
        # Generate verification token and link
        token = email_utils.generate_verification_token(email)
        verification_link = f"http://localhost:3000/verify-email?token={token}"
        
        print(f"\n{'='*60}")
        print(f"📧 VERIFICATION LINK FOR: {email}")
        print(f"{'='*60}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Status: {'Active' if user.is_active else 'Needs Verification'}")
        print(f"\n🔗 Verification Link:")
        print(f"{verification_link}")
        print(f"\n📋 Instructions:")
        print(f"1. Copy the link above")
        print(f"2. Paste it in your browser")
        print(f"3. Your account will be verified!")
        print(f"{'='*60}\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_verification_link.py user@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    get_verification_link(email)
