from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Worker
from database import get_db
from pydantic import BaseModel
from fastapi import APIRouter
router = APIRouter(prefix="/auth", tags=["auth"])

class SimpleLoginBody(BaseModel):
    id: int
    phone: str

@router.post("/simple-login")
def simple_login(body: SimpleLoginBody, db: Session = Depends(get_db)):
    worker = (
        db.query(Worker)
        .filter(Worker.id == body.id, Worker.phone == body.phone)
        .first()
    )
    if not worker:
        raise HTTPException(status_code=404, detail="工号或手机号错误")
    return {"token": f"fake-jwt-{worker.id}", "worker_id": worker.id}