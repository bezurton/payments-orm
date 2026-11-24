from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.controllers.payment_controller import router as payment_router
from app.exceptions import (
    DomainError,
    PaymentNotFoundError,
    InvoiceNotFoundError,
    InvoiceAlreadyPaidError,
    PaymentAmountExceedsBalanceError,
    InvalidPaymentStatusTransitionError,
    CompletedPaymentDeletionError,
)

app = FastAPI(title="Payments API", description=("REST API для управления платежами за коммунальные услуги управляющей организации"))

# Подключаем контроллер платежей
app.include_router(payment_router)

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    """Централизованная обработка доменных ошибок"""
    # Ошибки отсутствующих объектов
    if isinstance(exc, (PaymentNotFoundError, InvoiceNotFoundError)):
        status_code = 404

    # Ошибки бизнес-правил и конфликтов
    elif isinstance(exc,
        (
            InvoiceAlreadyPaidError,
            PaymentAmountExceedsBalanceError,
            InvalidPaymentStatusTransitionError,
            CompletedPaymentDeletionError,
        )
    ):
        status_code = 409
    else:
        status_code = 400
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": str(exc)
        }
    )