import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from core.config import settings
from core.logger import logger
from api.v1 import cameras

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered CCTV analysis backend for real-time pollution tracking.",
    version="1.0.0",
)


# Global Middleware for request tracing and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        f"HTTP {request.method} {request.url.path} completed status={response.status_code} processing_time={duration:.4f}s"
    )
    return response


# Centralized HTTP Exception Handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        f"HTTP error occurred: status={exc.status_code} detail={exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
            },
        },
    )


# Catch-all for unexpected internal server errors
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled system error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "An unexpected internal server error occurred.",
            },
        },
    )

app.include_router(cameras.router, prefix="/api/v1/cameras")

# Health Check Endpoint
@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "app": settings.APP_NAME,
    }