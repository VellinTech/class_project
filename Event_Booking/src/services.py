
import uuid
from typing import Dict

from fastapi import HTTPException

from src.models import BookingRequest, BookingResponse

EVENT_CAPACITY: Dict[str, Dict[str, int]] = {
    "sold out workshop": {"capacity": 1, "booked": 1},
    "limited concert":   {"capacity": 2, "booked": 0},
}


def _find_capacity_entry(event_name: str):
    return EVENT_CAPACITY.get(event_name.strip().lower())


def book_event(booking: BookingRequest) -> BookingResponse:
    entry = _find_capacity_entry(booking.event_name)
    seats_remaining = None

    if entry is not None:
        if entry["booked"] >= entry["capacity"]:
            raise HTTPException(
                status_code=409,
                detail=f"'{booking.event_name}' is fully booked — no seats remaining.",
            )
        entry["booked"] += 1
        seats_remaining = entry["capacity"] - entry["booked"]

    booking_id = f"bk_{uuid.uuid4().hex[:16]}"

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        attendee_name=booking.attendee_name,
        attendee_email=booking.attendee_email,
        event_name=booking.event_name,
        event_date=booking.event_date,
        event_location=booking.event_location,
        ticket_type=booking.ticket_type,
        seats_remaining=seats_remaining,
        message="Booking confirmed successfully.",
    )