from cars.models import Car
from cars.schema import CarCreateSchema, CarUpdateSchema
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status



def car_create(db: Session, car: CarCreateSchema):

    new_car = Car(
        make = car.make, 
                  model=car.model,
                  year=car.year
                  )
    
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


def car_list(db:Session):
    cars = db.query(Car).all()
    return cars


def car_detail(db:Session, car_id: int):
    car = db.query(Car).filter(Car.id==car_id).first()

    if not car:
        raise HTTPException(detail='Car not found', status_code=status.HTTP_404_NOT_FOUND)

    return car

def car_delete(db: Session, car_id: int):
    car = db.query(Car).filter(Car.id==car_id).first()

    if not car:
        raise HTTPException(detail='Car not found', status_code=status.HTTP_404_NOT_FOUND)
    db.delete(car)
    db.commit()

    return 'car deleted'


def car_update(db: Session, car_id: int, car_data: CarUpdateSchema):
    car = db.query(Car).filter(Car.id==car_id).first()

    if not car:
        raise HTTPException(detail='Car not found', status_code=status.HTTP_404_NOT_FOUND)
    
    # if car_data.make:
    #     car.make=car_data.make
    # if car_data.model:
    #     car.model=car_data.model
    # if car_data.year:
    #     car.year=car_data.year

    for key, value in car_data.dict().items():
        if value is not None:
            setattr(car, key, value)
    
    db.commit()
    db.refresh()

    response = {
        'msg': 'Updated',
        'status': status.HTTP_200_OK,
        'car': car,

    }

    return response

