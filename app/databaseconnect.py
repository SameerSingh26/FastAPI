from collections.abc import AsyncGenerator
import os
import uuid

from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import datetime
from dotenv import load_dotenv

load_dotenv()
database_name = "sql12836400"
database_host = "sql12.freesqldatabase.com"
database_port = 3306
database_user = os.getenv('SQL_USER')
database_password = os.getenv('SQL_PASSWORD')
Database_URL = f"mysql+asyncmy://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(Database_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    caption = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


async def create_database_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

            