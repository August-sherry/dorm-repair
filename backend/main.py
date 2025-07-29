# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine

# ---------- 数据库 ----------
engine = create_engine(
    "mssql+pyodbc://sa:1@127.0.0.1:1433/dorm?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# ---------- 应用 ----------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 路由 ----------
@app.get("/")
def root():
    return {"msg": "Dorm Repair API"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1")).fetchone()
    return "✅ SQL Server 连接成功"

# 报修
@app.post("/orders")
def create_order(order: dict, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO [order] (user_id, category_id, description) VALUES (:u, :c, :d)"),
        {"u": order["user_id"], "c": order["category_id"], "d": order["description"]}
    )
    db.commit()
    return {"ok": True}

# 工单列表
@app.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT o.id, o.description, o.status, c.default_priority, o.created_at
        FROM [order] o
        JOIN [category] c ON o.category_id = c.id
        ORDER BY c.default_priority DESC, o.created_at ASC
    """)).fetchall()
    return [
        {
            "id": r[0],
            "description": r[1],
            "status": r[2],
            "priority": r[3],
            "created_at": str(r[4])[:19]
        }
        for r in rows
    ]

# 接单
class TakeOrder(BaseModel):
    worker_id: int

@app.patch("/orders/{order_id}/take")
def take_order(order_id: int, body: TakeOrder, db: Session = Depends(get_db)):
    db.execute(
        text("UPDATE [order] SET worker_id=:w, status='processing' WHERE id=:id"),
        {"w": body.worker_id, "id": order_id}
    )
    db.commit()
    return {"ok": True}

# 完工
@app.patch("/orders/{order_id}/finish")
def finish_order(order_id: int, db: Session = Depends(get_db)):
    db.execute(
        text("UPDATE [order] SET status='done' WHERE id=:id"),
        {"id": order_id}
    )
    db.commit()
    return {"ok": True}

# 评价
class RateIn(BaseModel):
    order_id: int
    score: int
    comment: str

@app.post("/evaluations")
def rate_order(body: RateIn, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO evaluation (order_id, score, comment) VALUES (:o, :s, :c)"),
        {"o": body.order_id, "s": body.score, "c": body.comment}
    )
    db.commit()
    return {"ok": True}

# KPI 排行
@app.get("/kpi")
def get_kpi(db: Session = Depends(get_db)):
    sql = """
    SELECT w.id, w.phone AS name,
           ISNULL(AVG(CAST(e.score AS FLOAT)), 0) AS avg_score,
           COUNT(*) AS total
    FROM dbo.worker w
    JOIN dbo.[order] o  ON w.id = o.worker_id
    LEFT JOIN dbo.evaluation e ON o.id = e.order_id
    GROUP BY w.id, w.phone
    """
    rows = db.execute(text(sql)).fetchall()
    return [
        {"worker_id": r[0], "name": r[1], "avg_score": float(r[2]), "total": int(r[3])}
        for r in rows
    ]

# 维修工登录
class WorkerLogin(BaseModel):
    id: int
    phone: str

@app.post("/worker/login")
def worker_login(payload: WorkerLogin, db: Session = Depends(get_db)):
    worker = db.execute(
        text("SELECT id, phone FROM dbo.worker WHERE id = :id AND phone = :phone"),
        {"id": payload.id, "phone": payload.phone}
    ).fetchone()
    if not worker:
        raise HTTPException(400, "工号或手机号错误")
    return {"id": worker.id, "phone": worker.phone}
class AddWorkerIn(BaseModel):
    phone: str

@app.post("/admin/workers")
def add_worker(body: AddWorkerIn, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO dbo.worker(phone) VALUES (:phone)"),
        {"phone": body.phone}
    )
    db.commit()
    return {"ok": True}