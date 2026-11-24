from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from app.models.payment import Payment

class PaymentRepository:
    """Репозиторий для работы с платежами"""
    def __init__(self, session: Session):
        self.session = session

    def create(self, payment: Payment) -> Payment:
        """Добавление нового платежа в сессию"""
        self.session.add(payment)
        return payment

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Получение платежа по идентификатору"""
        return self.session.get(Payment, payment_id)

    def get_all(self) -> list[Payment]:
        """Получение всех платежей"""
        stmt = select(Payment).order_by(Payment.id)
        return list(self.session.scalars(stmt).all())

    def update_status(self, payment_id: int, new_status: str) -> Optional[Payment]:
        """Изменение статуса платежа"""
        payment = self.get_by_id(payment_id)
        if payment is None:
            return None
        payment.status = new_status
        return payment

    def delete(self, payment_id: int) -> bool:
        """Удаление платежа из сессии"""
        payment = self.get_by_id(payment_id)
        if payment is None:
            return False
        self.session.delete(payment)
        return True

    def get_by_status(self, status: str) -> list[Payment]:
        """Получение платежей по статусу"""
        stmt = select(Payment).where(Payment.status == status)
        return list(self.session.scalars(stmt).all())

    def get_completed_total_by_invoice(self, invoice_id: int) -> Decimal:
        """Получение суммы завершённых платежей"""
        stmt = select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.invoice_id == invoice_id,
            Payment.status == "completed")
        total = self.session.scalar(stmt)
        return Decimal(str(total or 0))

    def get_reserved_total_by_invoice(self, invoice_id: int, exclude_payment_id: Optional[int] = None) -> Decimal:
        """Получение суммы завершённых и ожидающих платежей"""
        stmt = select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.invoice_id == invoice_id,
            Payment.status.in_(["pending", "completed"]))
        if exclude_payment_id is not None:
            stmt = stmt.where(Payment.id != exclude_payment_id)
        total = self.session.scalar(stmt)
        return Decimal(str(total or 0))