from sqlmodel import Session, SQLModel, create_engine

from config.config import settings

SQLALCHEMY_DATABASE_URL = settings.DB_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Dependencies
def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
