from fastapi import FastAPI
from database import engine
from cars.router import router as car_router 
from cars.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(car_router, prefix='/car', tags=['car'])

@app.get('/')
def index():
    return {'msg': 'main func'}



    