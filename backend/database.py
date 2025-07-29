import os, pyodbc
from dotenv import load_dotenv
load_dotenv()

def test_conn():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')},1433;"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};PWD={os.getenv('DB_PASSWORD')};"
        f"TrustServerCertificate=yes"
    )
    conn = pyodbc.connect(conn_str, timeout=5)
    conn.close()
    return "✅ SQL Server 连接成功"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 用已有的 ODBC 参数拼出 SQLAlchemy URL
sqlalchemy_url = (
    "mssql+pyodbc://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_SERVER')}:1433/{os.getenv('DB_NAME')}?"
    "driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

engine = create_engine(sqlalchemy_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# FastAPI 依赖，供 routers 使用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()