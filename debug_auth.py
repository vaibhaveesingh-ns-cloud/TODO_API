#!/usr/bin/env python3
"""
Debug authentication issues
"""
from app.database import SessionLocal
from app.models import User
from app import auth, crud
from datetime import datetime, timedelta
import json

def check_user_status():
    """Check all users and their status"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("=== User Status Check ===")
        for user in users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Active: {user.is_active}")
            print(f"Admin: {user.is_admin}")
            print(f"Created: {user.created_at}")
            print("-" * 40)
        
        if not users:
            print("No users found in database!")
            print("You need to register a user first.")
        
        return users
    finally:
        db.close()

def test_token_generation(username: str):
    """Test token generation for a specific user"""
    db = SessionLocal()
    try:
        user = crud.get_user_by_username(db, username)
        if not user:
            print(f"User '{username}' not found!")
            return None
        
        if not user.is_active:
            print(f"User '{username}' is not active! Email verification required.")
            return None
        
        # Generate token
        token_data = {"sub": user.username}
        token = auth.create_access_token(data=token_data)
        
        print(f"=== Token Generated for {username} ===")
        print(f"Token: {token}")
        print(f"Expires in: {auth.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
        
        return token
    finally:
        db.close()

def activate_user(username: str):
    """Manually activate a user (for testing)"""
    db = SessionLocal()
    try:
        user = crud.get_user_by_username(db, username)
        if not user:
            print(f"User '{username}' not found!")
            return False
        
        if user.is_active:
            print(f"User '{username}' is already active!")
            return True
        
        crud.activate_user(db, user)
        print(f"User '{username}' has been activated!")
        return True
    finally:
        db.close()

def create_test_user():
    """Create a test user for debugging"""
    db = SessionLocal()
    try:
        # Check if test user exists
        existing = crud.get_user_by_username(db, "testuser")
        if existing:
            print("Test user already exists!")
            return existing
        
        # Create test user
        user = crud.create_user(db, "testuser", "test@example.com", "testpass123")
        # Activate immediately for testing
        crud.activate_user(db, user)
        print("Created and activated test user:")
        print(f"Username: testuser")
        print(f"Email: test@example.com")
        print(f"Password: testpass123")
        return user
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Authentication Debug Tool ===\n")
    
    # Check current users
    users = check_user_status()
    
    if not users:
        print("\nCreating test user...")
        create_test_user()
        users = check_user_status()
    
    # Test with first user or ask for username
    if users:
        first_user = users[0]
        print(f"\nTesting with user: {first_user.username}")
        
        if not first_user.is_active:
            print("Activating user for testing...")
            activate_user(first_user.username)
        
        token = test_token_generation(first_user.username)
        
        if token:
            print(f"\n=== Postman Instructions ===")
            print(f"1. POST to: http://localhost:8000/auth/token")
            print(f"2. Body (x-www-form-urlencoded):")
            print(f"   username: {first_user.username}")
            print(f"   password: [your_password]")
            print(f"3. Use returned access_token in Authorization header")
            print(f"4. Type: Bearer Token")
