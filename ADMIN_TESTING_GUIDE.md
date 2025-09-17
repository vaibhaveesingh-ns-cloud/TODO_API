# Admin Endpoints Testing Guide

This guide shows you how to test the admin endpoints in your TODO FastAPI application.

## Prerequisites

1. **Start the server:**
   ```bash
   python run_local.py
   ```

2. **Ensure you have an admin user:**
   - Run `python check_users.py` to see existing users
   - If no admin exists, the test script will create one automatically

## Admin Endpoints

### 1. GET /admin/users - List All Users

**Purpose:** Retrieve a list of all users in the system

**Authentication:** Requires admin token

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_active": true,
    "is_admin": true,
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": 2,
    "username": "testuser",
    "email": "testuser@example.com",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### 2. POST /admin/users/{user_id}/promote - Promote User to Admin

**Purpose:** Promote a regular user to admin status

**Authentication:** Requires admin token

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/admin/users/2/promote" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Expected Response:**
```json
{
  "id": 2,
  "username": "testuser",
  "email": "testuser@example.com",
  "is_active": true,
  "is_admin": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### 3. DELETE /admin/users/{user_id} - Delete User

**Purpose:** Delete a user from the system

**Authentication:** Requires admin token

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/admin/users/2" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Expected Response:**
```json
{
  "message": "User deleted"
}
```

## Getting an Admin Token

### Step 1: Login as Admin User
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Step 2: Extract Token from Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 3: Use Token in Subsequent Requests
Replace `YOUR_ADMIN_TOKEN` with the `access_token` value from step 2.

## Testing Methods

### Method 1: Automated Script
```bash
python test_admin_endpoints.py
```
This script will:
- Create an admin user if none exists
- Test all admin endpoints
- Show detailed results

### Method 2: Postman Collection

1. **Create a new collection in Postman**
2. **Add environment variables:**
   - `base_url`: `http://localhost:8000`
   - `admin_token`: (get from login request)

3. **Create requests:**

   **Login Request:**
   - Method: POST
   - URL: `{{base_url}}/auth/token`
   - Body (x-www-form-urlencoded):
     - username: `admin`
     - password: `admin123`
   - Test script to save token:
     ```javascript
     pm.test("Login successful", function () {
         pm.response.to.have.status(200);
         const response = pm.response.json();
         pm.environment.set("admin_token", response.access_token);
     });
     ```

   **List Users Request:**
   - Method: GET
   - URL: `{{base_url}}/admin/users`
   - Headers: `Authorization: Bearer {{admin_token}}`

   **Promote User Request:**
   - Method: POST
   - URL: `{{base_url}}/admin/users/2/promote`
   - Headers: `Authorization: Bearer {{admin_token}}`

   **Delete User Request:**
   - Method: DELETE
   - URL: `{{base_url}}/admin/users/2`
   - Headers: `Authorization: Bearer {{admin_token}}`

### Method 3: FastAPI Interactive Docs

1. **Open browser:** `http://localhost:8000/docs`
2. **Authenticate:**
   - Click "Authorize" button
   - Login with admin credentials
   - Use the returned token
3. **Test endpoints directly in the UI**

## Error Scenarios to Test

### 1. Unauthorized Access (No Token)
```bash
curl -X GET "http://localhost:8000/admin/users"
# Expected: 401 Unauthorized
```

### 2. Non-Admin User Token
```bash
# Login as regular user first, then try admin endpoint
curl -X GET "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer REGULAR_USER_TOKEN"
# Expected: 403 Forbidden
```

### 3. Invalid User ID
```bash
curl -X POST "http://localhost:8000/admin/users/999/promote" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
# Expected: 404 Not Found
```

### 4. Expired Token
```bash
# Use an old/expired token
curl -X GET "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer EXPIRED_TOKEN"
# Expected: 401 Unauthorized
```

## Troubleshooting

### No Admin User Exists
```bash
# Run the debug script to create one
python debug_auth.py

# Or manually create and promote a user
python -c "
from app.database import SessionLocal
from app import crud
db = SessionLocal()
user = crud.create_user(db, 'admin', 'admin@example.com', 'admin123')
crud.activate_user(db, user)
crud.promote_user_to_admin(db, user)
print('Admin user created!')
db.close()
"
```

### Server Not Running
```bash
python run_local.py
```

### Database Issues
```bash
# Check database status
python check_users.py

# Reset database if needed
rm todo_multiuser.db
alembic upgrade head
```

## Security Notes

- Admin tokens have the same expiration as regular tokens
- Always use HTTPS in production
- Admin operations are logged (if logging is configured)
- Be careful with user deletion - it's permanent
- Consider implementing soft deletes for production use
