from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    record_id = Column(Integer)
    object_id = Column(String)
    work_type = Column(String)
    period = Column(Date, nullable=True)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    contractor = Column(String)
