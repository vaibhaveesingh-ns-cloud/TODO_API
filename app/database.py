import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get database URL from environment variable with fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL")

# If no DATABASE_URL is set, use SQLite for local development
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./todo_multiuser.db"
    print("🔄 Using SQLite database for local development")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # For PostgreSQL (containerized or remote)
    if "postgresql" in DATABASE_URL.lower():
        print("🐘 Using PostgreSQL database")
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20
        )
    else:
        # Fallback for other database types
        engine = create_engine(DATABASE_URL)

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
        "is_sqlite": "sqlite" in DATABASE_URL.lower(),
        "pool_size": getattr(engine.pool, 'size', lambda: 'N/A')(),
        "checked_out": getattr(engine.pool, 'checkedout', lambda: 'N/A')()
    }
