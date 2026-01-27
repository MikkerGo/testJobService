from sqlalchemy.orm import Session
from app.models import Record


def is_exact_duplicate(session: Session, record: Record) -> bool:
    return session.query(Record).filter(
        Record.record_id == record.record_id,
        Record.object_id == record.object_id,
        Record.work_type == record.work_type,
        Record.period == record.period,
        Record.quantity == record.quantity,
        Record.unit_price == record.unit_price,
        Record.total_cost == record.total_cost,
        Record.contractor == record.contractor,
    ).first() is not None
