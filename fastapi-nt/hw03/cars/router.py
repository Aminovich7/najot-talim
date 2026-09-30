from fastapi import APIRouter, Depends
from cars.schema import CarCreateSchema, CarOutSchema,CarUpdateSchema
from sqlalchemy.orm import Session
from database import get_db
from cars.crud import car_create, car_list, car_detail, car_delete, car_update
from fastapi import status



router = APIRouter()


@router.post('/create', status_code= status.HTTP_201_CREATED, response_model= CarOutSchema)
def car_create_router(car: CarCreateSchema, db: Session = Depends(get_db)):
    return car_create(db, car)



@router.get('/list', response_model=list[CarOutSchema])
def car_list_router(db: Session = Depends(get_db)):
    return car_list(db)


@router.get('/detail/{car_id}', response_model=CarOutSchema)
def car_detail_router(car_id: int, db: Session = Depends(get_db)):
    return car_detail(car_id, db)


@router.delete('/delete/{car_id}')
def car_delete_router(car_id: int, db: Session = Depends(get_db)):
    return car_delete(car_id, db)

@router.patch('/update/{car_id}')
def car_update_router(car_id: int, car_data: CarUpdateSchema, db: Session = Depends(get_db)):
    return car_update(car_id, db)