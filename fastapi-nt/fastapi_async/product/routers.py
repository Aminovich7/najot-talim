from fastapi import APIRouter, Depends
from db import AsyncSession, get_db
from product.schema import ProductCreateSchema, ProductUpdateSchema
from product import crud

router = APIRouter(prefix='/products', tags=['Products'])


@router.post('/create')
async def create_product(
    data: ProductCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_product(data, db)


@router.get('/list')
async def list_product(
    db: AsyncSession = Depends(get_db)
):
    return await crud.list_product(db)


@router.get('/detail/{product_id}')
async def product_detail(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.product_detail(product_id, db)


@router.patch('/update/{product_id}')
async def product_update(
    product_id: int,
    data: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await crud.product_update(product_id, data, db)


@router.delete('/delete/{product_id}')
async def product_delete(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.product_delete(product_id, db)