from pydantic import BaseModel


class WatchCreateSchema(BaseModel):
    name: str
    country: str