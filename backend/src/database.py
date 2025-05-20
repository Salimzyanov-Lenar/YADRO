from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config import settings


engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()