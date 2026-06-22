# db/session.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres:sarah99@localhost:5431/postgres"

engine = create_engine(DATABASE_URL, echo=False)

with engine.connect() as conn:
  conn.execute(text("CREATE SCHEMA IF NOT EXISTS jobs"))
  conn.commit()

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)