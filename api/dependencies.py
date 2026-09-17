from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.create_db import default_db
from db.rep_relative import RelativeRepository
from db.rep_user import UserRepository


def get_user_repository(session: AsyncSession = Depends(default_db.get_session)):
    """Создаем "обертку" для users (Dependency)."""
    user_rep = UserRepository(session)

    return user_rep


def get_rel_repository(session: AsyncSession = Depends(default_db.get_session)):
    """Создаем "обертку" для relatives (Dependency)."""
    rel_rep = RelativeRepository(session)

    return rel_rep
