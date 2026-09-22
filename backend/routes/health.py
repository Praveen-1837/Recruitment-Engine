from datetime import datetime, timezone
from fastapi import APIRouter
from config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    """Health check endpoint returning service status, version, and timestamp."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
