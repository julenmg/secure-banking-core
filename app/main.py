from fastapi import FastAPI

from app.domain.bank import router as bank_router  # noqa: F401 — registers ORM models
from app.routers import users

app = FastAPI(
    title="Secure Banking API",
    version="1.0.0",
    description="Atomic transfers, compound interest, and full audit ledger.",
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(bank_router.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
