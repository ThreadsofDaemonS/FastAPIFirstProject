from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Load database URL from .env
DATABASE_URL = config('DATABASE_URL')

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session
async_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Function to get the async database session
async def get_db():
    async with async_session_local() as session:
        yield session
