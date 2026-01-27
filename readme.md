# Excel Service API (FastAPI + PostgreSQL)

## Описание
Сервис реализует REST API для:
- загрузки Excel-файлов;
- валидации данных и их нормализации;
- сохранения данных в базе PostgreSQL;
- получения данных с фильтрацией, сортировкой и применением limit/offset;
- экспорта сохранённых данных в формате JSON.

## Идеи решения
Принимается, что загружаемые Excel-файлы имеют указанную структуру, однако могут иметь пропуски, неверные типы данных или иные отклонения от эталона.
Для предотвращения ошибок каждая ячейка валидируется:
- ячейки, в которых ожидается числовое значение, избавляются от лишних символов (кавычек, пробелов и т.д.), в числах с плавающей точкой возможная запятая заменяется на точку ("2000,0"-> 2000.00);
- ячейки, в которых ожидаются строковые значения, избавляются от лишних пробелов;
- ячейки "object_id" должны иметь длину от 3 до 50 символов и не должны иметь иных символов кроме латинских букв, цифр, '_' и '-';
- ячейки "period" должны иметь корректную дату.
Данные, не прошедшие валидацию, не загружаются в базу, не прерывая загрузку корректных данных (каждая строка обрабатывается независимо).

Для предотвращения "захламления" базы одинаковые данные не загружаются (производится проверка на совпадение всех полей загружаемой строки с данными из базы).

## Архитектура
Для создания API используется FastAPI. Также он используется для экспорта данных в JSON.
Валидация выходных данных проходит с помощью Pydantic.
Для чтения файлов Excel используется Pandas+openpyxl, валидация проводится встроенными средствами Python (в том числе с помощью регулярных выражений).
Как было уопмянуто выше, в качестве базы данных используется PostgreSQL. Для взаимодействия с базой используется SQLAlchemy (ORM) + psycopg2.
В качестве сервера используется Uvicorn.

### Структура проекта
```
└───app
    ├───routers
    │   ├───records.py <- роутер получение данных из базы
    |   └───upload.py  <- роутер загрузки Excel-файлов
    ├───services
    │   ├───duplicator_checker <- проверка наличия в базе совпадающей записи
    |   ├───excel_parsers.py   <- методы для валидации и парсинга данных
    |   ├───excel_loader.py    <- загрузка Excel-файлов
    |   ├───filters.py         <- применение фильтрации для получения выходных данных
    |   └───query_utils.py     <- реализация limit/offset
    ├───database.py     <- подключение к базе
    ├───models.py       <- ORM-модель SQLAlchemy
    └───schemas.py      <- схема выходных данных для формирования JSON
```

### Схема таблицы в СУБД
```sql
records (
    id          SERIAL PRIMARY KEY,
    record_id   INTEGER,
    object_id   TEXT,
    work_type   TEXT,
    period      DATE,
    quantity    INTEGER,
    unit_price  NUMERIC(12, 2),
    total_cost  NUMERIC(12, 2),
    contractor  TEXT
)
```
Все поля являются обязательными.

## Инструкция для запуска
1. Клонировать репозиторий
```bash
git clone https://github.com/MikkerGo/testJobService.git
cd testJobService
```
2. Установить библиотеки

При необходимости создайте виртуальное окружение
```bash
pip install -r requirements.txt
```
3. Создать файл .env в корне проекта

Для примера используйте .env.example

4. Подготовить базу данных

Создайте базу 
```sql
CREATE DATABASE excel_db
```
Создайте таблицу 
```sql
CREATE TABLE IF NOT EXISTS records
(
    id integer NOT NULL,
    record_id integer,
    object_id text,
    work_type text,
    period date,
    quantity integer,
    unit_price numeric(12,2),
    total_cost numeric(12,2),
    contractor text,
    CONSTRAINT records_pkey PRIMARY KEY (id)
)
```
5. Запуск сервиса
```bash
uvicorn app.main:app --reload
```
В данный момент Swagger не отключён, поэтому он будет доступен по адресу 127.0.0.1:8000/docs

## Примеры использования
### Загрузка файла
```bash
curl -X POST http://127.0.0.1:8000/upload/excel \
  -F "file=@data.xlsx"
```
Пример ответа 
```json
{
  "inserted": 94,
  "total_rows": 95,
  "errors": [
    {
      "row": 21,
      "error": "Полный дубликат строки уже существует в базе"
    }
  ]
}
```
### Получение данных
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/records?contractor=Vendor%20A' \
  -H 'accept: application/json'
```
Пример ответа
```json
[
  {
    "record_id": 4,
    "object_id": "GH-890",
    "work_type": "upgrade",
    "period": "2022-04-01",
    "quantity": 9,
    "unit_price": 2876,
    "total_cost": 25884,
    "contractor": "Vendor A"
  },
  {
    "record_id": 5,
    "object_id": "HGFA",
    "work_type": "repair",
    "period": "2025-02-16",
    "quantity": 14,
    "unit_price": 1132,
    "total_cost": 15848,
    "contractor": "Vendor A"
  },
  {
    "record_id": 6,
    "object_id": "001-BJ",
    "work_type": "repair",
    "period": "2023-03-07",
    "quantity": 3,
    "unit_price": 6480,
    "total_cost": 19440,
    "contractor": "Vendor A"
  },
  {
    "record_id": 13,
    "object_id": "GH-891",
    "work_type": "install",
    "period": "2021-05-20",
    "quantity": 18,
    "unit_price": 4335,
    "total_cost": 78030,
    "contractor": "Vendor A"
  },
  {
    "record_id": 15,
    "object_id": "001-BJ",
    "work_type": "repair",
    "period": "2022-10-17",
    "quantity": 19,
    "unit_price": 4069,
    "total_cost": 77311,
    "contractor": "Vendor A"
  }
]
```
### Получение данных с фильтрацией
#### curl
```bash
curl -X GET http://127.0.0.1:8000/records?contractor=Vendor%20A&date_from=2022-02-25&date_to=2024-06-13&quantity_min=3&quantity_max=13&sort_by=period&sort_order=desc -H 'accept:application/json'
```
#### Браузер
```
http://127.0.0.1:8000/records?contractor=Vendor%20A&date_from=2022-02-25&date_to=2024-06-13&quantity_min=3&quantity_max=13&sort_by=period&sort_order=desc
```
Пример ответа
```json
[
  {
    "record_id": 6,
    "object_id": "001-BJ",
    "work_type": "repair",
    "period": "2023-03-07",
    "quantity": 3,
    "unit_price": 6480,
    "total_cost": 19440,
    "contractor": "Vendor A"
  },
  {
    "record_id": 4,
    "object_id": "GH-890",
    "work_type": "upgrade",
    "period": "2022-04-01",
    "quantity": 9,
    "unit_price": 2876,
    "total_cost": 25884,
    "contractor": "Vendor A"
  }
]
```
### Экспорт 
#### curl
```bash
curl -X GET http://127.0.0.1:8000/records/export -o records.json
```
#### Браузер
```
http://127.0.0.1:8000/records/export/
```
