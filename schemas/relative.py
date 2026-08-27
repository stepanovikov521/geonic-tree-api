from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ModelOfRelative(BaseModel):
    """."""

    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    patronymic: str | None = None
    gender: Literal["М", "Ж"]
    birth_date: date | None = None
    death_date: date | None = None
    biography: str | None = None
    photo_path: str | None = None
    father_id: int | None = None
    mother_id: int | None = None
    spouse_id: int | None = None


class ModelOfRelativeUpdate(BaseModel):
    """."""

    model_config = ConfigDict(from_attributes=True)
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    gender: Literal["М", "Ж"] | None = None
    birth_date: date | None = None
    death_date: date | None = None
    biography: str | None = None
    photo_path: str | None = None
    father_id: int | None = None
    mother_id: int | None = None
    spouse_id: int | None = None
