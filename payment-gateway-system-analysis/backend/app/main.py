from fastapi import FastAPI

from app.api.payments import router as payments_router

app = FastAPI(
    title="Payment Gateway API",
    description="Backend MVP for the payment gateway system analysis project.",
    version="1.0.0",
)

app.include_router(payments_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
