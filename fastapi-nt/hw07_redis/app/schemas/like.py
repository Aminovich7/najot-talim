from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class LikeOut(BaseModel):
    user_id: UUID
    post_id: UUID
    created_at: datetime