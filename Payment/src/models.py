import calendar
import re
from datetime import date

from pydantic import BaseModel, Field, field_validator

EXPIRATION_FORMAT_RE = re.compile(r"^(0[1-9]|1[0-2])/\d{2}$")


def _luhn_check(card_number: str) -> bool:
    """Standard Luhn checksum used by all major card networks."""
    digits = [int(d) for d in card_number]
    digits.reverse()
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


class PaymentRequest(BaseModel):
    amount: float = Field(
        ...,
        gt=0,
        le=1_000_000,
        description="Payment amount in USD. Must be greater than 0.",
    )
    card_number: str = Field(
        ...,
        min_length=13,
        max_length=19,
        description="Card number, digits only, 13-19 digits.",
    )
    expiration_date: str = Field(
        ...,
        description="Card expiration date in MM/YY format, e.g. '09/27'.",
    )
    cvv: str = Field(
        ...,
        min_length=3,
        max_length=4,
        description="Card verification value, 3 or 4 digits.",
    )

    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("card_number must contain only digits")
        if not _luhn_check(v):
            raise ValueError("card_number failed validation (not a valid card number)")
        return v

    @field_validator("cvv")
    @classmethod
    def validate_cvv(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("cvv must contain only digits")
        return v

    @field_validator("expiration_date")
    @classmethod
    def validate_expiration_date(cls, v: str) -> str:
        if not EXPIRATION_FORMAT_RE.match(v):
            raise ValueError("expiration_date must be in MM/YY format (e.g. '09/27')")

        month_str, year_str = v.split("/")
        month = int(month_str)
        year = 2000 + int(year_str)

        # Card is valid through the last calendar day of the expiration month.
        last_day = calendar.monthrange(year, month)[1]
        expiry_date = date(year, month, last_day)

        if expiry_date < date.today():
            raise ValueError(f"card has expired ({v})")

        return v


class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    amount: float
    card_last4: str