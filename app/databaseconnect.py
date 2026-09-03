from collections.abc import AsyncGenerator
import os
import uuid

from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import datetime
from dotenv import load_dotenv

load_dotenv()
Database_URL = f"mysql+asyncmy://{os.getenv('SQL_USER')}:{os.getenv('SQL_PASSWORD')}@sql12.freesqldatabase.com:3306/sql12836400"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(Database_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    caption = Column(String, nullable=False)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


async def create_database_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

            