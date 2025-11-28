# create_table.py

from sqlalchemy import create_engine
from models import Base  # make sure this import works

DATABASE_URL = "postgresql+psycopg2://postgres:mypassword@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")
