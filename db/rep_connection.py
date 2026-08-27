import os

from models.class_Base import Base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DataBaseManagerAsync:
    """Асинхронный класс базы данных."""

    def __init__(self) -> None:
        """."""
        # 1. Берем строку подключения из переменных окружения (которые мы прописали в docker-compose.yml)
        # Если переменная не задана, используем путь к SQLite по умолчанию (для работы вне Docker)
        db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./family_tree.db")

        # 2. Создаем движок. SQLAlchemy сам поймет, что если в строке есть postgresql,
        # то нужно использовать нужный драйвер.
        self.async_engine = create_async_engine(
            db_url,
            echo=False,  # Поставь True, если захочешь видеть SQL-запросы в логах Docker
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
