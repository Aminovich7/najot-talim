from fastapi import FastAPI

from books.routers import router as books_router


app = FastAPI()
app.include_router(books_router)
