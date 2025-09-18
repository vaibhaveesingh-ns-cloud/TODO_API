from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import todos, admin, users
from app.database import engine
from app import models
from app.scheduler import start_scheduler, stop_scheduler

# CORS configuration for local development
origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost"
]

# Create tables
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await start_scheduler()
    yield
    # Shutdown
    await stop_scheduler()

app = FastAPI(title="TaskMaster API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "taskmaster-backend"}
