from pydantic import BaseModel
from datetime import date

class RecordOut(BaseModel):
    record_id: int | None
    object_id: str | None
    work_type: str | None
    period: date | None
    quantity: int | None
    unit_price: float | None
    total_cost: float | None
    contractor: str | None

    class Config:
        from_attributes = True
