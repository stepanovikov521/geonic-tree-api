import logging
from core.config import logger
from models.models_relative import Relative
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class RelativeRepository:
    """Класс родственников."""

    def __init__(self, session: AsyncSession) -> None:
        """Переменная подключения."""
        self.session = session

    async def add_relative(self, data):
        """."""
        new_relative = Relative(**data)
        self.session.add(new_relative)
        await self.session.commit()
        await self.session.refresh(new_relative)
        return new_relative

    async def get_relative_by_id(self, relative_id):
        """."""
        stmt = (
            select(Relative)
            .where(Relative.id == relative_id)
            .options(
                joinedload(Relative.father),
                joinedload(Relative.mother),
                joinedload(Relative.spouse),
                selectinload(Relative.child_of_father),
                selectinload(Relative.child_of_mother),
            )
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_relative_by_name(self, rel_name):
        """."""
        stmt = (
            select(Relative)
            .where(Relative.first_name == rel_name)
            .options(
                joinedload(Relative.father),
                joinedload(Relative.mother),
                joinedload(Relative.spouse),
                selectinload(Relative.child_of_father),
                selectinload(Relative.child_of_mother),
            )
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def update_relative(self, relative_id, updated_data):
        """."""
        relative_obj = await self.session.get(Relative, relative_id)
        if relative_obj:
            for key, value in updated_data.items():
                setattr(relative_obj, key, value)
            await self.session.commit()
            await self.session.refresh(relative_obj)
            return relative_obj
        else:
            logger.warning(f"Родственник с ID {relative_id} не найден при обновлении")
            return None

    async def get_all_relatives(self):
        """."""
        stmt = select(Relative).options(
            joinedload(Relative.father),
            joinedload(Relative.mother),
            joinedload(Relative.spouse),
            selectinload(Relative.child_of_father),
            selectinload(Relative.child_of_mother),
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def delete_relative_id(self, relative_id):
        """."""
        relative_object = await self.session.get(Relative, relative_id)
        if relative_object:
            await self.session.delete(relative_object)
            await self.session.commit()
            return True
        else:
            return
