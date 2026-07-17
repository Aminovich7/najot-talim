"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.core.config import get_settings
from app.posts.routers import router as posts_router
from app.users.routers import auth_router, users_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Simple asynchronous Blog REST API",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Lightweight health endpoint."""
    return {"status": "ok"}
