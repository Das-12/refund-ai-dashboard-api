from fastapi import FastAPI, Request
from app.routes import auth, logs, roles, permissions, plans, subscriptions
from app.log_middleware import LoggingMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo
import traceback
import asyncio
from app.kafka_producer import send_app_error, init_kafka_producer, close_kafka_producer
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_kafka_producer()
        yield
    finally:
        await close_kafka_producer()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that logs unhandled exceptions to Kafka.
    """
    error_log = {
        "error_message": str(exc),
        "stack_trace": traceback.format_exc(),
        "path": request.url.path,
        "method": request.method,
        "client": request.client.host if request.client else "unknown",
        "service": 'dashboard_service',
        'timestamp': datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
    }
    asyncio.create_task(send_app_error(error_log))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please contact support."}
    )


app.include_router(auth.router, tags=["auth"])
app.include_router(logs.router, tags=["logs"])
app.include_router(roles.router, tags=["roles"])
app.include_router(permissions.router, tags=["permissions"])
app.include_router(plans.router, tags=["plans"])
app.include_router(subscriptions.router, tags=["subscriptions"])
app.add_middleware(LoggingMiddleware)