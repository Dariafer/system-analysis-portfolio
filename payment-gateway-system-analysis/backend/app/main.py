from fastapi import FastAPI

app = FastAPI(
    title="Payment Gateway API",
    description="Backend MVP for the payment gateway system analysis project.",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
