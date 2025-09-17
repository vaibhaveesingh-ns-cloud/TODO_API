#!/usr/bin/env python3
"""
Test script for Admin endpoints
Requires an admin user to be present in the database
"""
import requests
import json
from app.database import SessionLocal
from app.models import User
from app import crud

BASE_URL = "http://localhost:8000"

def get_admin_token():
    """Get authentication token for an admin user"""
    db = SessionLocal()
    try:
        # Find an admin user
        admin_user = db.query(User).filter(User.is_admin == True, User.is_active == True).first()
        
        if not admin_user:
            print("❌ No active admin user found!")
            print("Creating a test admin user...")
            
            # Create test admin user
            test_admin = crud.create_user(db, "admin", "admin@example.com", "admin123")
            crud.activate_user(db, test_admin)
            crud.promote_user_to_admin(db, test_admin)
            
            print("✅ Created test admin user:")
            print(f"   Username: admin")
            print(f"   Password: admin123")
            print(f"   Email: admin@example.com")
            
            admin_user = test_admin
        
        print(f"🔑 Using admin user: {admin_user.username}")
        
        # Get token
        login_data = {
            "username": admin_user.username,
            "password": "admin123"  # Default password for test admin
        }
        
        response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Successfully obtained admin token")
            return token
        else:
            print(f"❌ Failed to get token: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    finally:
        db.close()

def test_list_users(token):
    """Test GET /admin/users endpoint"""
    print("\n" + "="*50)
    print("🧪 Testing: GET /admin/users")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Success! Found {len(users)} users:")
        for user in users:
            print(f"   - ID: {user['id']}, Username: {user['username']}, Admin: {user['is_admin']}")
        return users
    else:
        print(f"❌ Failed: {response.text}")
        return []

def test_promote_user(token, user_id):
    """Test POST /admin/users/{user_id}/promote endpoint"""
    print("\n" + "="*50)
    print(f"🧪 Testing: POST /admin/users/{user_id}/promote")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/admin/users/{user_id}/promote", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Success! User promoted:")
        print(f"   - ID: {user['id']}, Username: {user['username']}, Admin: {user['is_admin']}")
        return user
    else:
        print(f"❌ Failed: {response.text}")
        return None

def test_delete_user(token, user_id):
    """Test DELETE /admin/users/{user_id} endpoint"""
    print("\n" + "="*50)
    print(f"🧪 Testing: DELETE /admin/users/{user_id}")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/admin/users/{user_id}", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! {result['message']}")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False

def create_test_user_for_testing():
    """Create a regular test user for testing admin operations"""
    db = SessionLocal()
    try:
        # Check if test user exists
        existing = crud.get_user_by_username(db, "testuser")
        if existing:
            print(f"Test user already exists (ID: {existing.id})")
            return existing.id
        
        # Create test user
        user = crud.create_user(db, "testuser", "testuser@example.com", "testpass123")
        crud.activate_user(db, user)
        print(f"✅ Created test user (ID: {user.id}) for admin operations")
        return user.id
    finally:
        db.close()

def main():
    """Main test function"""
    print("🚀 Starting Admin Endpoints Test")
    print("Make sure the FastAPI server is running on localhost:8000")
    print("-" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Server not responding. Make sure to run: python run_local.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run: python run_local.py")
        return
    
    # Get admin token
    token = get_admin_token()
    if not token:
        print("❌ Cannot proceed without admin token")
        return
    
    # Test 1: List all users
    users = test_list_users(token)
    
    # Test 2: Create a test user and promote them
    test_user_id = create_test_user_for_testing()
    if test_user_id:
        test_promote_user(token, test_user_id)
    
    # Test 3: List users again to see changes
    print("\n" + "="*50)
    print("🔄 Listing users after promotion:")
    print("="*50)
    test_list_users(token)
    
    # Test 4: Delete the test user (optional - uncomment if you want to test deletion)
    # print(f"\n⚠️  Would you like to delete test user (ID: {test_user_id})? [y/N]")
    # if input().lower() == 'y':
    #     test_delete_user(token, test_user_id)
    
    print("\n" + "="*60)
    print("✅ Admin endpoints testing completed!")
    print("="*60)

if __name__ == "__main__":
    main()
