from __future__ import annotations
from decimal import Decimal
from typing import Optional
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    bank_transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)

    invoice: Mapped["Invoice"] = relationship(
        back_populates="payments"
    )

    def __repr__(self):
        return (
            f"Payment(id={self.id}, "
            f"amount={self.amount}, "
            f"status='{self.status}')"
        )