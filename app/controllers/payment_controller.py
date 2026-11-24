from fastapi import APIRouter, Depends, Response, status
from app.dependencies import get_payment_service
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate,
)
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payload: PaymentCreate,
    service: PaymentService = Depends(get_payment_service)
):
    """Создание нового платежа"""
    return service.create(payload)

@router.get(
    "/",
    response_model=list[PaymentResponse]
)
def get_payments(
    service: PaymentService = Depends(get_payment_service)
):
    """Получение списка всех платежей"""
    return service.get_all()

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service)
):
    """Получение платежа по идентификатору"""
    return service.get_by_id(payment_id)

@router.patch(
    "/{payment_id}/status",
    response_model=PaymentResponse
)
def update_payment_status(
    payment_id: int,
    payload: PaymentStatusUpdate,
    service: PaymentService = Depends(get_payment_service)
):
    """Изменение статуса платежа"""
    return service.update_status(payment_id, payload.status)

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service)
):
    """Удаление платежа"""
    service.delete(payment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)