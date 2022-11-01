from contextvars import ContextVar

from configuration import CONFIG
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

bind = create_async_engine(
    f"postgresql+asyncpg://postgres:{CONFIG['DATABASE_PASSWORD']}@localhost:5432", echo=True)
_sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)
_base_model_session_ctx = ContextVar("session")
