import os
from pathlib import Path

from db.rep_connection import DataBaseManagerAsync

script_path = Path(__file__).resolve().parent
db_path = script_path / "family_tree.db"


def create_db_from_path(path: str | None = None):
    """Создание таблицы используя путь или переменную окружения."""
    # Если в тестах передали путь — берем его.
    # Иначе берем из переменных окружения (Docker) или локальный файл.
    if path and not path.startswith(("sqlite://", "postgresql://", "mysql://")):
        url = f"sqlite+aiosqlite:///{path}"
    else:
        url = path or os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")
    return DataBaseManagerAsync(db_url=url)


# Эта переменная будет использоваться в dependencies.py
default_db = create_db_from_path()
