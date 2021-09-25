from sqlmodel import SQLModel, create_engine
import config

sqlite_url = f"sqlite:///{config.DATABASE_NAME}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

