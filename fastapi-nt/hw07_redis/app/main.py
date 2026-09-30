from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import auth, posts, comments, likes, users, feed
from app.db.redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await close_redis()


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(likes.router, prefix="/likes", tags=["likes"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
