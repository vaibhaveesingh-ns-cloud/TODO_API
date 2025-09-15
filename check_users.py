#!/usr/bin/env python3
"""
Script to check database and list all users
"""
from app.database import SessionLocal, engine
from app.models import User, Todo
from sqlalchemy import text

def list_all_users():
    """List all users in the database"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\n=== Total Users: {len(users)} ===")
        print("-" * 80)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Active: {user.is_active}")
            print(f"Admin: {user.is_admin}")
            print(f"Created: {user.created_at}")
            
            # Count todos for this user
            todo_count = db.query(Todo).filter(Todo.owner_id == user.id).count()
            print(f"Todos: {todo_count}")
            print("-" * 40)
    finally:
        db.close()

def get_database_stats():
    """Get general database statistics"""
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        admin_users = db.query(User).filter(User.is_admin == True).count()
        total_todos = db.query(Todo).count()
        completed_todos = db.query(Todo).filter(Todo.completed == True).count()
        
        print("\n=== Database Statistics ===")
        print(f"Total Users: {user_count}")
        print(f"Active Users: {active_users}")
        print(f"Admin Users: {admin_users}")
        print(f"Total Todos: {total_todos}")
        print(f"Completed Todos: {completed_todos}")
        print(f"Pending Todos: {total_todos - completed_todos}")
    finally:
        db.close()

def check_database_tables():
    """Check what tables exist in the database"""
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        print("\n=== Database Tables ===")
        for table in tables:
            print(f"- {table[0]}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Checking TODO FastAPI Database...")
    check_database_tables()
    get_database_stats()
    list_all_users()
