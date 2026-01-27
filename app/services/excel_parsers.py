import pandas as pd
import re


class ExcelValidationError(Exception):
    pass


def require_value(value, field: str):
    if pd.isna(value):
        raise ExcelValidationError(f"Поле '{field}' пустое")
    if isinstance(value, str) and not value.strip():
        raise ExcelValidationError(f"Поле '{field}' пустое")
    return value


def clear_string(value: str):
    value = value.replace(" ", "").replace(",", ".").replace("\"", "").replace("\«", "").replace("\»", "")
    return value


def parse_float(value, field: str) -> float:
    value = require_value(value, field)

    if isinstance(value, str):
        value = clear_string(value)

    try:
        return float(value)
    except (TypeError, ValueError):
        raise ExcelValidationError(
            f"Поле '{field}' должно быть числом, получено: {value}"
        )
    

def parse_int(value, field: str) -> float:
    value = require_value(value, field)

    if isinstance(value, str):
        value = clear_string(value)

    try:
        return int(value)
    except (TypeError, ValueError):
        raise ExcelValidationError(
            f"Поле '{field}' должно быть числом, получено: {value}"
        )


def parse_str(value, field: str) -> str:
    value = require_value(value, field)
    return str(value).strip()


def parse_date(value, field: str):
    value = require_value(value, field)

    try:
        return pd.to_datetime(value).date()
    except Exception:
        raise ExcelValidationError(
            f"Поле '{field}' должно быть датой, получено: {value}"
        )
    

OBJECT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,50}$")


def parse_object_id(value, field: str) -> str:
    if pd.isna(value):
        raise ExcelValidationError("Поле 'object_id' пустое")

    value = str(value).strip()

    if not value:
        raise ExcelValidationError("Поле 'object_id' пустое")

    if not OBJECT_ID_PATTERN.match(value):
        raise ExcelValidationError(
            f"Неверный формат object_id: '{value}'"
        )

    return value
