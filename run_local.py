#!/usr/bin/env python3
"""
Local development runner for TaskMaster backend
This script sets up the environment for local development without Docker
"""

import os
import sys
from pathlib import Path

def setup_local_env():
    """Set up environment variables for local development"""
    # Load local environment variables
    env_local = Path(".env.local")
    if env_local.exists():
        print("📁 Loading local environment variables...")
        with open(env_local) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    
    # Ensure DATABASE_URL is not set for SQLite fallback
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
        print("🗑️  Removed DATABASE_URL to use SQLite for local development")
    
    print("✅ Environment configured for local development")

def main():
    """Main function to run the backend locally"""
    setup_local_env()
    
    # Import and run the app
    try:
        import uvicorn
        from app.main import app
        
        print("🚀 Starting TaskMaster backend locally...")
        print("📍 Backend will be available at: http://localhost:8000")
        print("📚 API docs will be available at: http://localhost:8000/docs")
        print("🗄️  Using SQLite database: ./todo_multiuser.db")
        print("\n" + "="*50)
        
        uvicorn.run(
            "app.main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print(f"❌ Error importing dependencies: {e}")
        print("💡 Make sure you've installed requirements: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
