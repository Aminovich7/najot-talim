from fastapi import HTTPException, status

from books.models import Book, Comment, Saved
from users.models import User


def _require_owner(owner_id: int | None, current_user: User, resource_name: str) -> None:
    if owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not own this {resource_name}",
        )


def require_book_owner(book: Book, current_user: User) -> None:
    _require_owner(book.owner_id, current_user, "book")


def require_comment_owner(comment: Comment, current_user: User) -> None:
    _require_owner(comment.user_id, current_user, "comment")


def require_saved_owner(saved: Saved, current_user: User) -> None:
    _require_owner(saved.user_id, current_user, "saved item")
