from sqlalchemy.orm import Query
from sqlalchemy import asc, desc
from app.models import Record

SORT_FIELDS = {
    "record_id": Record.record_id,
    "object_id": Record.object_id,
    "work_type": Record.work_type,
    "period": Record.period,
    "quantity": Record.quantity,
    "unit_price": Record.unit_price,
    "total_cost": Record.total_cost,
    "contractor": Record.contractor,
}


def apply_sorting(
    query: Query,
    sort_by: str | None,
    sort_order: str = "asc",
):
    if not sort_by:
        return query

    column = SORT_FIELDS.get(sort_by)
    if not column:
        return query

    if sort_order == "desc":
        return query.order_by(desc(column))

    return query.order_by(asc(column))


def apply_limit_or_offset(
    query: Query,
    limit: int = 50,
    offset: int = 0,
):
    limit = min(limit, 1000)  # защита от перегруза
    return query.limit(limit).offset(offset)
