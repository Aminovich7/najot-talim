from watches.models import Watch
from watches.schema import WatchCreateSchema
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException



def watch_create(db: Session, watch: WatchCreateSchema):
    new_watch = Watch(
        name=watch.name,
        country=watch.country
    )
    db.add(new_watch)
    db.commit()
    db.refresh(new_watch)
    return new_watch

def watch_list(db:Session):
    watches = db.query(Watch).all()
    return watches