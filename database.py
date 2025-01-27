# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
#
# SQL_DB_URL = "sqlite:///./db.sqlite3"
#
# engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})
#
# session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/fastapi_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with async_session_local() as session:
        yield session
