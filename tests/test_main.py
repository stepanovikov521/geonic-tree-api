from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from db.create_db import create_db_from_path
from services.main_API_async import app

script_path = Path(__file__).resolve().parent
test_db_path = script_path / "test_family_tree.db"


# Указываем pytest, что фикстура будет асинхронной
# scope="module" означает, что вся эта цепочка выполняется один раз на весь файл с тестами.
# Все функции-тесты в этом файле работают с одной и той же созданной базой данных по очереди.
# Если бы стоял scope="function" (значение по умолчанию), то база создавалась и удалялась бы заново перед каждым тестом.
@pytest.fixture(scope="function")
async def async_client():
    """Фикстура: создаёт тестовую БД и асинхронный клиент."""
    test_db = create_db_from_path(str(test_db_path))

    # 1. Создаём базу данных тестовую
    await test_db.create_tables()

    import db.create_db

    db.create_db.default_db = test_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client  # Здесь побегут наши тесты

    # 2. После тестов закрываем все соединения, чтобы файл не блокировался
    await (
        test_db.close()
    )  # Если в твоем DataBaseManagerAsync есть метод закрытия соединения

    # 3. Удаляем временный файл
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.mark.asyncio
async def test_read_rot(async_client: AsyncClient):
    """Тест корневого эндпоинта."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Привет! Наш сервер генеалогического древа успешно запущен!"
    }


@pytest.mark.asyncio
async def test_get_non_existent_relative(async_client: AsyncClient):
    """Тест поиска несуществующего родственника."""
    response = await async_client.get("/relatives/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Родственник с ID 9999 не найден"}


@pytest.mark.asyncio
async def test_create_relative(async_client: AsyncClient):
    """Тест успешного создания родственника."""
    new_person = {"first_name": "Иван", "last_name": "Иванов", "gender": "М"}
    response = await async_client.post("/relatives/", json=new_person)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["first_name"] == "Иван"
    assert data["last_name"] == "Иванов"
    assert data["gender"] == "М"


@pytest.mark.asyncio
async def test_create_relative_child(async_client: AsyncClient):
    """Тест успешного создания ребёнка."""
    new_person = {
        "first_name": "Макс",
        "last_name": "Иванов",
        "gender": "М",
        "father_id": 1,
    }
    response = await async_client.post("/relatives/", json=new_person)
    assert response.status_code == 200
    data = response.json()
    print("ОТВЕТ ПРИ СОЗДАНИИ РЕБЁНКА:", data)
    assert isinstance(data["id"], int)
    assert data["first_name"] == "Макс"
    assert data["last_name"] == "Иванов"
    assert data["gender"] == "М"
    assert data["father_id"] == 1


@pytest.mark.asyncio
async def test_delete_relative(async_client: AsyncClient):
    """Тест на удаление родственника."""
    new_person = {"first_name": "Мааксим", "last_name": "Максимов", "gender": "М"}

    response_new = await async_client.post("/relatives/", json=new_person)
    assert response_new.status_code == 200

    created_id = response_new.json()["id"]
    response_del = await async_client.delete(f"/relatives/{created_id}")
    assert response_del.status_code == 200

    response_get = await async_client.get(f"/relatives/{created_id}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_id_parents_is_null(async_client: AsyncClient):
    """Тест на преобразование id отца в пустоту после удаления отца."""
    new_person = {"first_name": "Мааксим", "last_name": "Максимов", "gender": "М"}
    response_new_1 = await async_client.post("/relatives/", json=new_person)
    assert response_new_1.status_code == 200

    new_person = {
        "first_name": "Макс",
        "last_name": "Иванов",
        "gender": "М",
        "father_id": 1,
    }
    response_new_2 = await async_client.post("/relatives/", json=new_person)
    assert response_new_2.status_code == 200
    assert response_new_2.json()["father_id"] == 1

    created_id = response_new_2.json()["id"]
    response_del = await async_client.delete(f"/relatives/{created_id}")
    assert response_del.status_code == 200

    response_get = await async_client.get(f"/relatives/{created_id}")
    assert response_get.status_code == 404

    response = await async_client.get("/relatives/1")
    data = response.json()
    assert data["father_id"] is None
