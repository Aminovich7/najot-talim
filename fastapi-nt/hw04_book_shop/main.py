from fastapi import FastAPI

from books.comments_router import router as comments_router
from books.routers import router as books_router
from books.saved_router import router as saved_router
from users.routers import router as users_router


app = FastAPI()
app.include_router(books_router)
app.include_router(comments_router)
app.include_router(saved_router)
app.include_router(users_router)
