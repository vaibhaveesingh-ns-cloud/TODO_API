from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, get_database_info
from .routers import users as users_router, todos as todos_router, admin as admin_router
from .middleware import log_requests

Base.metadata.create_all(bind=engine)  # create tables for demo; use Alembic for migrations

app = FastAPI(title="TaskMaster API", description="A collaborative todo application", version="1.0.0")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)  # optional

app.include_router(users_router.router)
app.include_router(todos_router.router)
app.include_router(admin_router.router)

@app.get("/")
def read_root():
    return {"message": "TaskMaster API is running!", "docs": "/docs"}

@app.get("/health")
def health_check():
    """Health check endpoint with database info"""
    db_info = get_database_info()
    return {
        "status": "healthy",
        "database": {
            "type": "PostgreSQL" if db_info["is_postgresql"] else "SQLite",
            "connected": True
        },
        "version": "1.0.0"
    }
