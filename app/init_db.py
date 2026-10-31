"""Create the local database tables for this starter project.

Run with: python -m app.init_db
For production systems, use Alembic migrations instead.
"""
from .database import Base, engine
from . import models  # noqa: F401 - registers models with SQLAlchemy metadata

Base.metadata.create_all(bind=engine)
print("Database tables created.")
