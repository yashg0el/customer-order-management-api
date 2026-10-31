# Customer & Order Management API

A portfolio backend project demonstrating REST API design, CRUD operations, relational data modelling, request validation, PostgreSQL integration and automated tests.

## Tech stack
- Python 3.11+
- FastAPI and Pydantic v2
- PostgreSQL 16
- SQLAlchemy 2.x
- Pytest and FastAPI TestClient
- Docker Compose (local PostgreSQL)

## Features
- Customer CRUD: create, list, retrieve, update and delete
- Product CRUD: create, list, retrieve, update and delete
- Order creation and order listing/retrieval
- Pydantic validation for email, required fields, SKU format, positive prices/quantities and stock
- Database constraints and unique email/SKU handling
- HTTP error handling: 404 for missing records, 409 for duplicates/insufficient stock, 422 for invalid input
- Pagination using `skip` and `limit`
- Automated API tests for CRUD, validation, duplicate records and inventory updates

## Run locally

### 1. Create a virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL
```bash
docker compose up -d db
```

The default connection string is:
`postgresql+psycopg://postgres:postgres@localhost:5432/customer_api`

For a different database, copy `.env.example` to `.env` and set `DATABASE_URL`. Export the variable in your shell before starting the app (or load it with your preferred dotenv setup).

### 3. Create tables and start the API
```bash
python -m app.init_db
uvicorn app.main:app --reload
```
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

### 4. Run automated tests
```bash
pytest -v
```
Tests use an isolated in-memory SQLite database through dependency overrides, so the test suite does not need a running PostgreSQL instance. The application itself defaults to PostgreSQL. The schema is created explicitly with `python -m app.init_db`; importing the API does not connect to or modify the database.

## Example API requests

Create a customer:
```bash
curl -X POST http://127.0.0.1:8000/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"Asha Sharma","email":"asha@example.com","phone":"9876543210"}'
```

Create a product:
```bash
curl -X POST http://127.0.0.1:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Wireless Mouse","sku":"MOUSE-001","price":"799.00","stock":10}'
```

Create an order (replace IDs with returned IDs):
```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"product_id":1,"quantity":2}'
```

## Suggested interview walkthrough
1. Explain the resource model: customers, products and orders, with foreign-key relationships.
2. Explain the request lifecycle: FastAPI route -> Pydantic schema validation -> SQLAlchemy session -> PostgreSQL -> response model.
3. Explain why validation exists at two layers: Pydantic catches malformed requests; database constraints protect persisted data.
4. Explain transaction handling for orders: verify customer/product, check stock, decrement inventory and insert the order in one transaction.
5. Explain tests: `TestClient` exercises HTTP endpoints; dependency overrides inject an isolated test database.
6. Discuss next production improvements: Alembic migrations, authentication/authorization, structured logging, rate limiting, Dockerfile and CI pipeline.

## Important honesty note
Only list features you have personally run, tested and can explain. The test suite in this starter project is provided, but run it locally and resolve any environment issues before claiming that all tests pass. Do not describe this portfolio project as production experience.
