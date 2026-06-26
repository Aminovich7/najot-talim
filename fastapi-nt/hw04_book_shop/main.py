from fastapi import FastAPI

from books.authors_router import router as authors_router
from books.categories_router import router as categories_router
from books.comments_router import router as comments_router
from books.routers import router as books_router
from books.saved_router import router as saved_router
from users.routers import router as users_router


app = FastAPI(
    title="Book Shop API",
    description="Book shop service with users, authors, categories, books, comments, and saved items.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"persistAuthorization": True},
    openapi_tags=[
        {"name": "users", "description": "Authentication, profile, and account actions."},
        {"name": "authors", "description": "Author management and author-linked books."},
        {"name": "categories", "description": "Category management and category-linked books."},
        {"name": "books", "description": "Book CRUD, search, and book-linked views."},
        {"name": "comments", "description": "Comment CRUD and comment listings."},
        {"name": "saved", "description": "Saved-item endpoints."},
    ],
)
app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(books_router)
app.include_router(comments_router)
app.include_router(saved_router)
app.include_router(users_router)
