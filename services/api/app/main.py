import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import configure_logging, get_settings
from app.routes import catchup, draft_reply, extract_asks, health, summarize, thoughtpartner, triage

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger("inbox_triage.api")

app = FastAPI(title=settings.app_name, version="0.1.0")

app.include_router(health.router)
app.include_router(triage.router)
app.include_router(summarize.router)
app.include_router(extract_asks.router)
app.include_router(draft_reply.router)
app.include_router(catchup.router)
app.include_router(thoughtpartner.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid4())
    start_time = time.perf_counter()

    logger.info(
        "request_started",
        extra={"event": "request_started", "method": request.method, "path": request.url.path},
    )

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "request_failed",
            extra={"event": "request_failed", "method": request.method, "path": request.url.path},
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error", "requestId": request_id})

    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        f"request_completed in {duration_ms}ms",
        extra={
            "event": "request_completed",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
        },
    )
    return response
