from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from pydantic import BaseModel
from backend.database import SessionLocal          # 你的 SQLAlchemy Session

router = APIRouter(prefix="/worker", tags=["worker"])

class LoginIn(BaseModel):
    phone: str

@router.post("/login")
def worker_login(body: LoginIn):
    with SessionLocal() as db:
        row = db.execute(
            text("SELECT id, phone FROM dbo.worker WHERE phone = :p"),
            {"p": body.phone}
        ).fetchone()
        if not row:
            raise HTTPException(status_code=422, detail="手机号不存在")
    return {"id": row.id, "phone": row.phone}