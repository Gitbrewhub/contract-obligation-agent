import os

from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://contract_user:contract_password@localhost:5432/contracts_db",
)

engine = create_engine(DATABASE_URL)
