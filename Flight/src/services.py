from src.models import BookingRequest

# Simulated store of bookings (in-memory, resets on restart).
bookings = []

# Arbitrary limit used to simulate a flight running out of a given
# seat preference, so the booking process has something to reject.
SEATS_PER_PREFERENCE = 3


def count_matching_bookings(flight_number, flight_date, seat_preference):
    count = 0

    for booking in bookings:
        same_flight = booking["flight_number"] == flight_number
        same_date = booking["flight_date"] == flight_date
        same_seat_type = booking["seat_preference"] == seat_preference

        if same_flight and same_date and same_seat_type:
            count = count + 1

    return count


def generate_booking_reference():
    next_number = len(bookings) + 1
    return "BKG" + str(next_number).zfill(6)


def book_flight(request: BookingRequest):
    # Returns a tuple: (success, message, booking_reference)
    # booking_reference is None when the booking is not successful.

    existing_bookings = count_matching_bookings(
        request.flight_number,
        request.flight_date,
        request.seat_preference,
    )

    if existing_bookings >= SEATS_PER_PREFERENCE:
        return False, "No " + request.seat_preference + " seats available on this flight", None

    booking_reference = generate_booking_reference()

    bookings.append({
        "booking_reference": booking_reference,
        "passenger_name": request.passenger_name,
        "age": request.age,
        "contact_number": request.contact_number,
        "origin": request.origin,
        "destination": request.destination,
        "flight_number": request.flight_number,
        "flight_date": request.flight_date,
        "seat_preference": request.seat_preference,
    })

    return True, "Flight booked successfully", booking_reference