from sqlalchemy import select
from product.schema import ProductCreateSchema, ProductOutSchema, ProductUpdateSchema
from db import AsyncSession
from product.models import Product
from fastapi import status

async def create_product(data: ProductCreateSchema, db: AsyncSession):
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return {
        'msg': 'Product created successfully',
        'status': status.HTTP_201_CREATED,
        'data': ProductOutSchema.model_validate(product)
    }


async def list_product(db: AsyncSession):
    query = select(Product)
    result = await db.execute(query)
    products = result.scalars().all()
    await db.commit()

    return {
        'msg': 'Products list',
        'count': len(products),
        'status': status.HTTP_200_OK,
        'data': products
    }






async def get_product_or_404(product_id: int, db: AsyncSession) -> Product:
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found"
        )
    return product


async def product_detail(product_id: int, db: AsyncSession):
    product = await get_product_or_404(product_id, db)
    return {
        'msg': 'Product detail',
        'status': status.HTTP_200_OK,
        'data': ProductOutSchema.model_validate(product)
    }


async def product_update(product_id: int, data: ProductUpdateSchema, db: AsyncSession):
    product = await get_product_or_404(product_id, db)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return {
        'msg': 'Product updated successfully',
        'status': status.HTTP_200_OK,
        'data': ProductOutSchema.model_validate(product)
    }


async def product_delete(product_id: int, db: AsyncSession):
    product = await get_product_or_404(product_id, db)

    await db.delete(product)
    await db.commit()

    return {
        'msg': 'Product deleted successfully',
        'status': status.HTTP_204_NO_CONTENT
    }