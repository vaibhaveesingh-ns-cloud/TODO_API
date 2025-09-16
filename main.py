{{ ... }}
from fastapi.middleware.cors import CORSMiddleware
{{ ... }}

# CORS configuration for containerized deployment
origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost",
    "http://frontend:80",
    "http://nginx:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

{{ ... }}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "taskmaster-backend"}
