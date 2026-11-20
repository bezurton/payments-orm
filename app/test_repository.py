from decimal import Decimal
from uuid import uuid4
from app.database import SessionLocal
from app.models import Resident, Invoice, Payment
from app.repositories import PaymentRepository

def main():
    session = SessionLocal()
    try:
        resident = Resident(
            full_name="Иван Иванов",
            email=f"ivan-{uuid4().hex[:8]}@example.com",
            apartment_number="101"
        )
        session.add(resident)
        session.commit()
        session.refresh(resident)
        print("Создан жилец:", resident)

        invoice = Invoice(
            description="Коммунальные услуги",
            amount=Decimal("4500.00"),
            billing_period="2026-11",
            status="unpaid",
            resident_id=resident.id
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        print("Создано начисление:", invoice)

        payment = Payment(
            amount=Decimal("4500.00"),
            payment_method="bank_card",
            status="pending",
            bank_transaction_id="TEST-TRANSACTION-001",
            invoice_id=invoice.id
        )
        repository = PaymentRepository(session)
        created_payment = repository.create(payment)
        print("Создан платёж:", created_payment)

        found_payment = repository.get_by_id(created_payment.id)
        print("Найден платёж:", found_payment)

        updated_payment = repository.update_status(
            created_payment.id,
            "completed"
        )
        print("Обновлённый платёж:", updated_payment)

        all_payments = repository.get_all()
        print("Все платежи:", all_payments)

        completed_payments = repository.get_by_status("completed")
        print("Завершённые платежи:", completed_payments)

        deleted = repository.delete(created_payment.id)
        print("Платёж удалён:", deleted)

        session.delete(invoice)
        session.commit()

        session.delete(resident)
        session.commit()

        print("\nВсе операции успешно выполнены!")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()