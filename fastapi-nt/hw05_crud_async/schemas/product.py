from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0

    class ProductCreate(ProductBase):
        pass

    class ProductUpdate(BaseModel):
        name: str | None = None
        description: str | None = None
        price: float | None = None
        stock: int | None = None


    class ProductRead(ProductBase):
        id: int
        model_config = ConfigDict(from_attributes=True)
