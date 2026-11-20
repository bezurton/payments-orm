from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Resident(Base):
    __tablename__ = "residents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    apartment_number: Mapped[str] = mapped_column(String(20), nullable=False)

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="resident"
    )

    def __repr__(self):
        return (
            f"Resident(id={self.id}, "
            f"full_name='{self.full_name}', "
            f"apartment='{self.apartment_number}')"
        )
