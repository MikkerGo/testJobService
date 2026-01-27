from sqlalchemy.orm import Query
from app.models import Record
from datetime import date


def apply_filters(
    query: Query,
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
):
    if record_id is not None:
        query = query.filter(Record.record_id == record_id)

    if object_id:
        query = query.filter(Record.object_id == object_id)

    if work_type:
        query = query.filter(Record.work_type == work_type)

    if contractor:
        query = query.filter(Record.contractor == contractor)

    if date_from:
        query = query.filter(Record.period >= date_from)

    if date_to:
        query = query.filter(Record.period <= date_to)

    if quantity_min is not None:
        query = query.filter(Record.quantity >= quantity_min)

    if quantity_max is not None:
        query = query.filter(Record.quantity <= quantity_max)

    if unit_price_min is not None:
        query = query.filter(Record.unit_price >= unit_price_min)

    if unit_price_max is not None:
        query = query.filter(Record.unit_price <= unit_price_max)

    if total_cost_min is not None:
        query = query.filter(Record.total_cost >= total_cost_min)

    if total_cost_max is not None:
        query = query.filter(Record.total_cost <= total_cost_max)

    return query
