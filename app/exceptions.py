class DomainError(Exception):
    """Базовое исключение бизнес-логики"""
    pass

class PaymentNotFoundError(DomainError):
    """Платёж не найден"""
    pass

class InvoiceNotFoundError(DomainError):
    """Начисление не найдено"""
    pass

class InvoiceAlreadyPaidError(DomainError):
    """Начисление уже полностью оплачено"""
    pass

class PaymentAmountExceedsBalanceError(DomainError):
    """Сумма платежа превышает доступный остаток"""
    pass

class InvalidPaymentStatusTransitionError(DomainError):
    """Недопустимое изменение статуса платежа"""
    pass


class CompletedPaymentDeletionError(DomainError):
    """Нельзя удалить завершённый платёж"""
    pass