from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate
from app.repositories.payment_repository import PaymentRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.exceptions import (
    PaymentNotFoundError,
    InvoiceNotFoundError,
    InvoiceAlreadyPaidError,
    PaymentAmountExceedsBalanceError,
    InvalidPaymentStatusTransitionError,
    CompletedPaymentDeletionError,
)

class PaymentService:
    """Сервис для управления платежами и бизнес-логикой"""
    def __init__(self, payment_repository: PaymentRepository, invoice_repository: InvoiceRepository):
        self.payment_repository = payment_repository
        self.invoice_repository = invoice_repository
        # Репозитории используют одну сессию БД
        self.session: Session = payment_repository.session

    def create(self, data: PaymentCreate) -> Payment:
        """Создание платежа с проверкой бизнес-правил"""
        try:
            # Проверяем существование начисления.
            invoice = self.invoice_repository.get_by_id(data.invoice_id)
            if invoice is None:
                raise InvoiceNotFoundError(f"Начисление с ID {data.invoice_id} не найдено.")
            invoice_amount = Decimal(str(invoice.amount))
            # Проверяем, не оплачено ли начисление
            completed_total = (self.payment_repository.get_completed_total_by_invoice(invoice.id))
            if (invoice.status == "paid" or completed_total >= invoice_amount):
                raise InvoiceAlreadyPaidError(f"Начисление {invoice.id} уже оплачено.")
            # Считаем уже зарезервированные суммы
            reserved_total = (self.payment_repository.get_reserved_total_by_invoice(invoice.id))
            remaining = invoice_amount - reserved_total
            # Проверяем, не превышает ли платёж остаток
            if data.amount > remaining:
                raise PaymentAmountExceedsBalanceError(f"Сумма платежа {data.amount} превышает доступный остаток {remaining}.")
            # Создаём новый платёж
            payment = Payment(
                amount=data.amount,
                payment_method=data.payment_method,
                status="pending",
                bank_transaction_id=data.bank_transaction_id,
                invoice_id=data.invoice_id
            )
            self.payment_repository.create(payment)
            # Сервис управляет транзакцией
            self.session.commit()
            self.session.refresh(payment)
            return payment
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, payment_id: int) -> Payment:
        """Получение платежа по идентификатору"""
        payment = self.payment_repository.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundError(f"Платёж с ID {payment_id} не найден.")
        return payment

    def get_all(self) -> list[Payment]:
        """Получение всех платежей"""
        return self.payment_repository.get_all()

    def update_status(self, payment_id: int,new_status: str) -> Payment:
        """Изменение статуса платежа"""
        try:
            payment = self.payment_repository.get_by_id(payment_id)
            if payment is None:
                raise PaymentNotFoundError(f"Платёж с ID {payment_id} не найден.")
            # Разрешаем переход только из pending
            if payment.status != "pending":
                raise InvalidPaymentStatusTransitionError("Изменять статус можно только у платежа со статусом pending.")
            if new_status not in ("completed", "failed"):
                raise InvalidPaymentStatusTransitionError(f"Недопустимый новый статус: {new_status}.")
            if new_status == "completed":
                invoice = self.invoice_repository.get_by_id(payment.invoice_id)
                if invoice is None:
                    raise InvoiceNotFoundError(f"Начисление {payment.invoice_id} не найдено.")
                if invoice.status == "paid":
                    raise InvoiceAlreadyPaidError("Это начисление уже полностью оплачено.")
                invoice_amount = Decimal(str(invoice.amount))
                completed_before = (self.payment_repository.get_completed_total_by_invoice(invoice.id))
                if completed_before >= invoice_amount:
                    raise InvoiceAlreadyPaidError("Начисление уже полностью оплачено.")
                # Проверяем остаток без учёта текущего платежа
                other_reserved = (self.payment_repository.get_reserved_total_by_invoice(
                        invoice.id,
                        exclude_payment_id=payment.id)
                )
                remaining = invoice_amount - other_reserved
                if payment.amount > remaining:
                    raise PaymentAmountExceedsBalanceError(f"Сумма платежа {payment.amount} превышает доступный остаток {remaining}.")
            # Меняем статус платежа
            self.payment_repository.update_status(payment_id, new_status)
            # Если платеж завершён и начисление полностью оплачено, меняем статус начисления
            if (new_status == "completed" and completed_before + payment.amount >= invoice_amount):
                self.invoice_repository.update_status(invoice.id,"paid")
            self.session.commit()
            self.session.refresh(payment)
            return payment
        except Exception:
            self.session.rollback()
            raise

    def delete(self, payment_id: int) -> bool:
        """Удаление платежа с проверкой его статуса"""
        try:
            payment = self.payment_repository.get_by_id(payment_id)
            if payment is None:
                raise PaymentNotFoundError(f"Платёж с ID {payment_id} не найден.")
            if payment.status == "completed":
                raise CompletedPaymentDeletionError("Нельзя удалить завершённый платёж.")
            self.payment_repository.delete(payment_id)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise