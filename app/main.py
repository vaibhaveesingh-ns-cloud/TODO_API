from fastapi import FastAPI
from .database import engine, Base
from .routers import users as users_router, todos as todos_router, admin as admin_router
from .middleware import log_requests

Base.metadata.create_all(bind=engine)  # create tables for demo; use Alembic for migrations

app = FastAPI(title="Todo Multiuser API")

app.middleware("http")(log_requests)  # optional

app.include_router(users_router.router)
app.include_router(todos_router.router)
app.include_router(admin_router.router)

