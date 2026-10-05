from fastapi import FastAPI

from src.models import FeePaymentRequest, FeePaymentResponse
from src import services


app = FastAPI(
    title="Student Fee Payment API",
    description="Process student fee payments with full request validation.",
)


@app.post(
    "/fees/pay",
    response_model=FeePaymentResponse,
    tags=["Fee Payments"]
)
def process_fee_payment(
    payment: FeePaymentRequest
) -> FeePaymentResponse:
    """
    Process a student fee payment.
    """
    return services.process_fee_payment(payment)


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Student Fee Payment API - visit /docs for Swagger UI"
    }