from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.payment import Payment
from typing import Optional

class PaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, payment: Payment) -> Payment:
        try:
            self.session.add(payment)
            self.session.commit()
            self.session.refresh(payment)
            return payment
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.session.get(Payment, payment_id)

    # Получение всех платежей
    def get_all(self) -> list[Payment]:
        stmt = select(Payment).order_by(Payment.id)
        return list(self.session.scalars(stmt).all())

    def update_status(
        self,
        payment_id: int,
        new_status: str
    ) -> Optional[Payment]:

        payment = self.get_by_id(payment_id)
        if payment is None:
            return None
        try:
            payment.status = new_status
            self.session.commit()
            self.session.refresh(payment)
            return payment
        except Exception:
            self.session.rollback()
            raise

    def delete(self, payment_id: int) -> bool:
        payment = self.get_by_id(payment_id)
        if payment is None:
            return False
        try:
            self.session.delete(payment)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_by_status(self, status: str) -> list[Payment]:
        stmt = select(Payment).where(
            Payment.status == status
        )
        return list(self.session.scalars(stmt).all())