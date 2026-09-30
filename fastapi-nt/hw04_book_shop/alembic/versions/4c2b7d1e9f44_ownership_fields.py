"""ownership fields

Revision ID: 4c2b7d1e9f44
Revises: 2a3f1a9c8b10
Create Date: 2026-06-26 00:00:00.000001
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4c2b7d1e9f44"
down_revision: Union[str, Sequence[str], None] = "2a3f1a9c8b10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("books", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_books_owner_id"), "books", ["owner_id"], unique=False)
    op.create_foreign_key(
        "fk_books_owner_id_users",
        "books",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.add_column("comments", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_comments_user_id"), "comments", ["user_id"], unique=False)
    op.create_foreign_key(
        "fk_comments_user_id_users",
        "comments",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.add_column("saveds", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_saveds_user_id"), "saveds", ["user_id"], unique=False)
    op.create_foreign_key(
        "fk_saveds_user_id_users",
        "saveds",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint("uq_saveds_user_book", "saveds", ["user_id", "book_id"])


def downgrade() -> None:
    op.drop_constraint("uq_saveds_user_book", "saveds", type_="unique")
    op.drop_constraint("fk_saveds_user_id_users", "saveds", type_="foreignkey")
    op.drop_index(op.f("ix_saveds_user_id"), table_name="saveds")
    op.drop_column("saveds", "user_id")

    op.drop_constraint("fk_comments_user_id_users", "comments", type_="foreignkey")
    op.drop_index(op.f("ix_comments_user_id"), table_name="comments")
    op.drop_column("comments", "user_id")

    op.drop_constraint("fk_books_owner_id_users", "books", type_="foreignkey")
    op.drop_index(op.f("ix_books_owner_id"), table_name="books")
    op.drop_column("books", "owner_id")
