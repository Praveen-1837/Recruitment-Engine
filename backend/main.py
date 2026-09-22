import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config import settings
from models.database import init_db
from routes.health import router as health_router
from routes.jobs import router as jobs_router
from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from routes.results import router as results_router

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("recruitment_engine")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    logger.info("Initializing database tables...")
    init_db()
    logger.info("Recruitment Intelligence Engine backend initialized successfully.")
    yield
    logger.info("Shutting down backend...")

# Ensure tables are created on import/startup
init_db()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered resume screening, skill extraction, and candidate ranking engine.",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows frontend on port 3000 / dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Consistent JSON Error Handlers (Rules.md Section 1.4)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    if isinstance(detail, dict) and "error" in detail:
        return JSONResponse(status_code=exc.status_code, content=detail)
    
    code = "HTTP_ERROR"
    if exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 400:
        code = "BAD_REQUEST"
    elif exc.status_code == 413:
        code = "FILE_TOO_LARGE"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "code": code,
            "message": str(detail),
            "details": {}
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_msgs = [f"{e.get('loc', ['field'])[-1]}: {e.get('msg', 'invalid')}" for e in errors]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "code": "VALIDATION_ERROR",
            "message": "; ".join(error_msgs),
            "details": {"validation_errors": errors}
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred. Please try again.",
            "details": {"error_type": type(exc).__name__}
        }
    )

# Register API Routers
app.include_router(health_router)
app.include_router(jobs_router)
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(results_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
