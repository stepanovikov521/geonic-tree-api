from models.class_Base import Base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DataBaseManagerAsync:
    """Асинхроный класс базы данных."""

    def __init__(self, db_path) -> None:
        """Переменная подключения."""
        self.db_path = db_path
        self.async_engine = create_async_engine(
            f"sqlite+aiosqlite:///{db_path}?foreign_keys=on",
            echo=False,  # Поставьте True для отладки SQL-запросов в консоли
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
