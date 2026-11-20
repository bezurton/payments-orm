from __future__ import annotations
from decimal import Decimal
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    billing_period: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="unpaid", nullable=False)
    resident_id: Mapped[int] = mapped_column(ForeignKey("residents.id"), nullable=False)

    resident: Mapped["Resident"] = relationship(
        back_populates="invoices"
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="invoice"
    )

    def __repr__(self):
        return (
            f"Invoice(id={self.id}, "
            f"amount={self.amount}, "
            f"status='{self.status}')"
        )