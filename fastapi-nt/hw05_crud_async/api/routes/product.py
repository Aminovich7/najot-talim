from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

from crud.product import (
    get_product,
    list_products,
    create_product,
    update_product,
    delete_product,
)

from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=list[ProductRead])
async def get_products(
    db: AsyncSession = Depends(get_db),
):
    return await list_products(db)

@router.get("/{product_id}", response_model=ProductRead)
async def get_single_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    product = await get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product

@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_product(db, data)


@router.put("/{product_id}", response_model=ProductRead)
async def update_existing_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    product = await get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return await update_product(
        db,
        product,
        data,
    )



@router.delete("/{product_id}")
async def remove_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    product = await get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    await delete_product(db, product)

    return {
        "message": "Product deleted successfully"
    }