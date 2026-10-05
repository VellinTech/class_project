import re
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z\s'-]{1,99}$")


class TicketType(str, Enum):
    GENERAL = "general"
    VIP = "vip"
    STUDENT = "student"
    GROUP = "group"


class BookingRequest(BaseModel):
    # ── Attendee ────────────────────────────────────────────
    attendee_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Attendee's full name — letters, spaces, hyphens, apostrophes only.",
    )
    attendee_email: EmailStr = Field(..., description="Attendee's email address.")
    attendee_age: int = Field(
        ...,
        ge=1,
        le=120,
        description="Attendee's age in years.",
    )

    # ── Event ───────────────────────────────────────────────
    event_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Name of the event, e.g. 'Summer Jazz Concert'.",
    )
    event_date: str = Field(
        ...,
        description="Event date in YYYY-MM-DD format. Must not be in the past.",
    )
    event_location: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Venue or location of the event.",
    )

    # ── Ticket ──────────────────────────────────────────────
    ticket_type: TicketType = Field(
        ...,
        description="One of: general, vip, student, group.",
    )

    @field_validator("attendee_name")
    @classmethod
    def validate_attendee_name(cls, v: str) -> str:
        v = v.strip()
        if not NAME_RE.match(v):
            raise ValueError(
                "attendee_name must start with a letter and contain only "
                "letters, spaces, hyphens, or apostrophes"
            )
        return v

    @field_validator("event_name")
    @classmethod
    def validate_event_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("event_name cannot be blank or whitespace-only")
        return v

    @field_validator("event_location")
    @classmethod
    def validate_event_location(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("event_location cannot be blank or whitespace-only")
        return v

    @field_validator("event_date")
    @classmethod
    def validate_event_date(cls, v: str) -> str:
        try:
            parsed = datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("event_date must be in YYYY-MM-DD format")
        if parsed < date.today():
            raise ValueError(f"event_date ({v}) cannot be in the past")
        return v

    @model_validator(mode="after")
    def validate_student_ticket_age(self):
        if self.ticket_type == TicketType.STUDENT and not (5 <= self.attendee_age <= 30):
            raise ValueError(
                "student ticket_type requires attendee_age between 5 and 30"
            )
        return self


class BookingResponse(BaseModel):
    booking_id: str
    status: str
    attendee_name: str
    attendee_email: EmailStr
    event_name: str
    event_date: str
    event_location: str
    ticket_type: TicketType
    seats_remaining: int | None = Field(
        None, description="Seats left for this event, if capacity is tracked."
    )
    message: str