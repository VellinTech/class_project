import uuid

from fastapi import HTTPException

from src.models import PaymentRequest, PaymentResponse

# Well-known dummy test card numbers (published by real payment
# processors specifically for testing declines) mapped to a reason.
DECLINED_TEST_CARDS = {
    "4000000000000002": "Card declined by issuer.",
    "4000000000009995": "Insufficient funds.",
    "4000000000000119": "Processing error — please try again.",
}


def process_payment(payment: PaymentRequest) -> PaymentResponse:
    """
    Simulate authorization against a payment gateway.

    Raises:
        HTTPException(402) if the card is a known "declined" test card.
    """
    if payment.card_number in DECLINED_TEST_CARDS:
        raise HTTPException(
            status_code=402,
            detail=DECLINED_TEST_CARDS[payment.card_number],
        )

    # Simulated "authentication" step — in a real integration this is
    # where you'd call out to the card network / processor.
    transaction_id = f"txn_{uuid.uuid4().hex[:16]}"

    return PaymentResponse(
        transaction_id=transaction_id,
        status="approved",
        message="Payment processed successfully.",
        amount=payment.amount,
        card_last4=payment.card_number[-4:],
    )