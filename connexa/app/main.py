from fastapi import FastAPI
from app.core.config import settings

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.dependencies import get_db
from app.users.router import router as users_router



app = FastAPI(
            title = settings.APP_NAME,
            version=settings.API_VERSION,
            )

app.include_router(users_router)


@app.get("/")
async def root():
    return {
        "msg": "Welcome to Connexa"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/db-check")
async def database_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }