from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.payment_repository import PaymentRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.services.payment_service import PaymentService

def get_db() -> Generator[Session, None, None]:
    """Создание и закрытие сессии базы данных"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_payment_service(
    session: Session = Depends(get_db)
) -> PaymentService:
    """Создание сервиса платежей с необходимыми репозиториями"""
    payment_repository = PaymentRepository(session)
    invoice_repository = InvoiceRepository(session)
    return PaymentService(
        payment_repository=payment_repository,
        invoice_repository=invoice_repository
    )