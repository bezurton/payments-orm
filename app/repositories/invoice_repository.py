from typing import Optional
from sqlalchemy.orm import Session
from app.models.invoice import Invoice

class InvoiceRepository:
    """Репозиторий для работы с начислениями"""
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Получение начисления по идентификатору"""
        return self.session.get(Invoice, invoice_id)
    def update_status(self, invoice_id: int, new_status: str) -> Optional[Invoice]:
        """Изменение статуса начисления"""
        invoice = self.get_by_id(invoice_id)
        if invoice is None:
            return None
        invoice.status = new_status
        return invoice