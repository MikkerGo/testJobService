from fastapi import APIRouter, Query
from datetime import date
from app.database import SessionLocal
from app.models import Record
from app.schemas import RecordOut
from app.services.filters import apply_filters
from app.services.query_utils import apply_sorting, apply_limit_or_offset

router = APIRouter(prefix="/records", tags=["records"])


@router.get("", response_model=list[RecordOut])
def get_records(
    # фильтры
    record_id: int | None = None,
    object_id: str | None = None,
    work_type: str | None = None,
    contractor: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    quantity_min: float | None = None,
    quantity_max: float | None = None,
    unit_price_min: float | None = None,
    unit_price_max: float | None = None,
    total_cost_min: float | None = None,
    total_cost_max: float | None = None,

    # сортировка
    sort_by: str | None = Query(None, description="Поле сортировки"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),

    # пагинация
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    session = SessionLocal()
    query = session.query(Record)

    query = apply_filters(
        query,
        record_id=record_id,
        object_id=object_id,
        work_type=work_type,
        contractor=contractor,
        date_from=date_from,
        date_to=date_to,
        quantity_min=quantity_min,
        quantity_max=quantity_max,
        unit_price_min=unit_price_min,
        unit_price_max=unit_price_max,
        total_cost_min=total_cost_min,
        total_cost_max=total_cost_max,
    )

    query = apply_sorting(query, sort_by, sort_order)
    query = apply_limit_or_offset(query, limit, offset)

    result = query.all()
    session.close()
    return result
