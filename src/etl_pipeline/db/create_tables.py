# create_tables.py (or inside main once)
from models import Base
from session import engine

Base.metadata.create_all(bind=engine)