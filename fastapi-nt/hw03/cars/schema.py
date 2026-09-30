from pydantic import BaseModel


class CarCreateSchema(BaseModel):
    make: str
    model: str
    year:  int


class CarOutSchema(BaseModel):
    id: int
    make: str
    model: str
    year:  int



class CarUpdateSchema(BaseModel):
    make: str
    model: str
    year:  int