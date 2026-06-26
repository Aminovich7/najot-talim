from fastapi import FastAPI

from books.routers import router as books_router
from users.routers import router as users_router


app = FastAPI()
app.include_router(books_router)
app.include_router(users_router)
