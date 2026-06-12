from fastapi import FastAPI
from database import engine
from watches.router import router as watch_router 
from watches.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(watch_router, prefix='/watch', tags=['watch'])

@app.get('/')
def index():
    return {'msg': 'main func'}


