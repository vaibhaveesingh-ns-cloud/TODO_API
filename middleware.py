from fastapi import Request
import time

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"{request.method} {request.url} completed_in={process_time:.2f}ms status={response.status_code}")
    return response
