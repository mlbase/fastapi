from sqlalchemy import create_engine, future
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
import logging
import os

load_dotenv()
DB_USERNAME: str = os.getenv("DB_USERNAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT")
DB_DATABASE: str = os.getenv("DB_DATABASE")
SQLALCHEMY_DATABASE_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

engine = create_async_engine(f"{SQLALCHEMY_DATABASE_URL}", pool_size=10, echo=True, pool_pre_ping=True)
session = AsyncSession(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)





