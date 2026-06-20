from fastapi import FastAPI

from app.api.payments import router as payments_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend MVP for the payment gateway system analysis project.",
    version=settings.app_version,
)

app.include_router(payments_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
    }
