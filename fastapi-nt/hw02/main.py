from fastapi import FastAPI
from watches.models import Watch
from database import engine


app = FastAPI()

watches.models.Base.metadata.create_all(bind=engine)


@app.get('/')
def index():
    return {'msg': 'main func'}
