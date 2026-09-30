from fastapi import APIRouter, Depends
from watches.schema import WatchCreateSchema
from sqlalchemy.orm import Session
from database import get_db
from watches.crud import watch_create, watch_list



router = APIRouter()


@router.post('/create')
def watch_create_router(watch: WatchCreateSchema, db: Session = Depends(get_db)):
    return watch_create(db, watch)



@router.post('/list')
def watch_list_router(db: Session = Depends(get_db)):
    return watch_list(db)




