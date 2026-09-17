from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_rel_repository
from core.exceptions import AppError, EntityNotFoundError
from db.rep_relative import RelativeRepository
from schemas.relative import ModelOfRelative, ModelOfRelativeUpdate

router = APIRouter(prefix="/relatives", tags=["Родственники"])


@router.get("/{relative_id}")
async def read_root_rel_id(
    relative_id: int, rel_rep: RelativeRepository = Depends(get_rel_repository)
):
    """Поиск родственника по id."""
    id_rel = await rel_rep.get_relative_by_id(relative_id)
    if not id_rel:
        raise EntityNotFoundError("Родственник", relative_id)

    return id_rel


@router.get("/")
async def read_all_relatives(rel_rep: RelativeRepository = Depends(get_rel_repository)):
    """Просмотр всех родственников в базе."""
    all_rel = await rel_rep.get_all_relatives()

    return all_rel


@router.post("/")
async def add_new_rel(
    person: ModelOfRelative, rel_rep: RelativeRepository = Depends(get_rel_repository)
):
    """Добавление нового родственника онлайн."""
    person_dict = person.model_dump()
    created_person = await rel_rep.add_relative(person_dict)
    return created_person


@router.patch("/{relative_id}")
# Если надо поменять полностью, то надо использовать @app.put, иначе @app.patch

async def update_rel(
    relative_id: int,
    person: ModelOfRelativeUpdate,
    rel_rep: RelativeRepository = Depends(get_rel_repository),
):
    """Обновление данных родственника."""
    person_dict = person.model_dump(exclude_unset=True)
    if not person_dict:
        raise AppError("Не введены изменения для родственника.", status_code=400)
    updated_person = await rel_rep.update_relative(relative_id, person_dict)
    if updated_person is None:
        raise EntityNotFoundError("Родственник", relative_id)
    return updated_person


@router.delete("/{relative_id}")
async def delete_rel(
    relative_id: int, rel_rep: RelativeRepository = Depends(get_rel_repository)
):
    """Удаление родственника."""
    deleted_rel = await rel_rep.delete_relative_id(relative_id)
    if deleted_rel is None:
        raise EntityNotFoundError("Родственник", relative_id)
    return {"message": f"Родственник с ID {relative_id} успешно удален из древа"}
