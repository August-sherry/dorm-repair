from sqlalchemy.orm import Session

import schemas
from models import Order

def create_order(db: Session, obj: schemas.OrderCreate):
    db_order = Order(**obj.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order