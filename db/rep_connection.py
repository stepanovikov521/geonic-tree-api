import os

from models.class_Base import Base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DataBaseManagerAsync:
    """Асинхронный класс базы данных."""

    def __init__(self, db_url: str | None = None) -> None:
        """."""
        # 1. Логика выбора URL:
        # Если мы в тестах и передали путь (например, "sqlite:///test.db"), используем его.
        # Если мы в Docker и передали DATABASE_URL через переменные окружения — используем его.
        # Если ничего не передано — используем стандартный SQLite локально.

        if db_url:
            self.db_url = db_url
        else:
            self.db_url = os.getenv(
                "DATABASE_URL", "sqlite+aiosqlite:///./family_tree.db"
            )

        # 2. Создаем движок
        # Важно: SQLAlchemy сам поймет, что делать, если в строке есть postgresql или sqlite
        self.async_engine = create_async_engine(
            self.db_url,
            echo=False,  # Включи True на время отладки SQL запросов в Docker
        )

        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def create_tables(self):
        """Создание таблиц в БД."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self):
        """Создание сессии для подключения."""
        async with self.AsyncSessionLocal() as session:
            yield session

    async def close(self):
        """Закрывает все соединения с базой данных."""
        await self.async_engine.dispose()
