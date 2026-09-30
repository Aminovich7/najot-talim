from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status

async def get_product(db: AsyncSession, product_id: int)-> Product | None: 
    result = await db.execute(select(Product).where(Product.id == product_id))

    return result.scalar_one_or_none()

async def list_products(db: AsyncSession):

    # Build the SQL query
    query = select(Product)

    # Execute the query
    result = await db.execute(query)

    # Convert database rows into Product objects
    products = result.scalars().all()

    # Return the products
    return products

async def create_product(db: AsyncSession, data: ProductCreate):
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def update_product(
    db: AsyncSession,
    product: Product,
    data: ProductUpdate
):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    await db.commit()

    await db.refresh(product)

    return product



async def delete_product(
    db: AsyncSession,
    product: Product,
):
    await db.delete(product)

    await db.commit()

