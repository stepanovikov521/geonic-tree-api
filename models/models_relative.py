from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.class_Base import Base


class Relative(Base):
    """Чертёж родственника."""

    __tablename__ = "people"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    patronymic: Mapped[str | None] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String, CheckConstraint("gender IN ('М', 'Ж')"))

    # Исправлено здесь: убрали GLOB, оставили просто строки.
    # База данных теперь создастся успешно!
    birth_date: Mapped[date | None] = mapped_column(Date)
    death_date: Mapped[date | None] = mapped_column(Date)

    biography: Mapped[str | None] = mapped_column(String)
    photo_path: Mapped[str | None] = mapped_column(String)
    father_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("people.id", ondelete="SET NULL")
    )
    mother_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("people.id", ondelete="SET NULL")
    )
    spouse_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("people.id", ondelete="SET NULL")
    )
    father: Mapped["Relative | None"] = relationship(
        "Relative",
        remote_side=[id],
        foreign_keys=[father_id],
        back_populates="child_of_father",
    )
    mother: Mapped["Relative | None"] = relationship(
        "Relative",
        remote_side=[id],
        foreign_keys=[mother_id],
        back_populates="child_of_mother",
    )
    spouse: Mapped["Relative | None"] = relationship(
        "Relative",
        foreign_keys=[spouse_id],
        back_populates="spouse_of",
    )
    spouse_of: Mapped["Relative | None"] = relationship(
        "Relative",
        remote_side=[id],
        foreign_keys=[spouse_id],
        back_populates="spouse",
    )
    child_of_father: Mapped[list["Relative | None"]] = relationship(
        "Relative", foreign_keys=[father_id], back_populates="father"
    )
    child_of_mother: Mapped[list["Relative | None"]] = relationship(
        "Relative", foreign_keys=[mother_id], back_populates="mother"
    )

    def get_full_name(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"
