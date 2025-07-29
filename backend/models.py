from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    description = Column(String)
    img_urls = Column(String)
    priority = Column(Integer, default=0)
    status = Column(String, default="pending")
class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)        # 如果暂时不用可留空
    phone = Column(String(20), unique=True, nullable=False)
    phone_verified = Column(Integer, default=0)     # SQL Server BIT 用 0/1
    sms_code = Column(String(6), nullable=True)
    sms_expire = Column(DateTime, nullable=True)