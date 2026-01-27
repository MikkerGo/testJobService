import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Record
from app.services.excel_parsers import (
    parse_float,
    parse_int,
    parse_str,
    parse_date,
    ExcelValidationError
)


REQUIRED_COLUMNS = [
    "record_id",
    "object_id",
    "work_type",
    "period",
    "quantity",
    "unit_price",
    "total_cost",
    "contractor",
]


async def load_excel(file):
    df = pd.read_excel(file.file)
    print(df.head())
    print(df.dtypes)

    # 1. Проверка структуры
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Отсутствуют колонки: {missing}")

    session: Session = SessionLocal()

    inserted = 0
    errors = []

    try:
        for idx, row in df.iterrows():
            try:
                record = Record(
                    record_id=parse_int(row["record_id"], "record_id"),
                    object_id=parse_str(row["object_id"], "object_id"),
                    work_type=parse_str(row["work_type"], "work_type"),
                    period=parse_date(row["period"], "period"),
                    quantity=parse_int(row["quantity"], "quantity"),
                    unit_price=parse_float(row["unit_price"], "unit_price"),
                    total_cost=parse_float(row["total_cost"], "total_cost"),
                    contractor=parse_str(row["contractor"], "contractor"),
                )
                print(record)
                print(record.id, record.object_id, record.work_type, record.period, record.quantity,
                      record.unit_price, record.total_cost, record.contractor)

                session.add(record)
                inserted += 1

            except ExcelValidationError as e:
                errors.append({
                    "row": idx + 2,
                    "error": str(e)
                })

        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return {
        "inserted": inserted,
        "errors": errors,
        "total_rows": len(df)
    }
