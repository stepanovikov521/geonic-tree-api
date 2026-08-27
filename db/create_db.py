from pathlib import Path

from db.rep_connection import DataBaseManagerAsync

script_path = Path(__file__).resolve().parent
db_path = script_path / "family_tree.db"


def create_bd_from_path(path: str | None = None):
    """Создание таблицы используя путь."""
    if path is None:
        path = str(db_path)
    return DataBaseManagerAsync(path)


default_db = create_bd_from_path()
