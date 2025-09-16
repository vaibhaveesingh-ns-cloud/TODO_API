import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get database URL from environment variable or use default PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://taskmaster_user:taskmaster_password@localhost:5432/taskmaster"
)

# For SQLite fallback (development only)
SQLITE_DATABASE_URL = "sqlite:///./todo_multiuser.db"

# Use PostgreSQL by default, fallback to SQLite if PostgreSQL is not available
try:
    # Try PostgreSQL connection
    engine = create_engine(DATABASE_URL)
    # Test the connection
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    print(f"✅ Connected to PostgreSQL database")
except Exception as e:
    print(f"⚠️  PostgreSQL connection failed: {e}")
    print("🔄 Falling back to SQLite database")
    DATABASE_URL = SQLITE_DATABASE_URL
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_database_info():
    """Get information about the current database connection"""
    return {
        "database_url": DATABASE_URL,
        "engine": str(engine.url),
        "is_postgresql": "postgresql" in DATABASE_URL.lower(),
        "is_sqlite": "sqlite" in DATABASE_URL.lower()
    }
