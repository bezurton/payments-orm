from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field

class PaymentBase(BaseModel):
    """Общие поля платежа"""
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    payment_method: str = Field(min_length=1, max_length=50)
    invoice_id: int = Field(gt=0)
    bank_transaction_id: Optional[str] = Field(default=None, max_length=100)

class PaymentCreate(PaymentBase):
    """Данные для создания нового платежа"""
    pass

class PaymentStatusUpdate(BaseModel):
    """Данные для изменения статуса платежа"""
    status: Literal["completed", "failed"]

class PaymentResponse(PaymentBase):
    """Ответ API с информацией о платеже"""
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)