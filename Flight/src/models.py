from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime

VALID_SEAT_PREFERENCES = ["Window", "Aisle", "Middle"]


class BookingRequest(BaseModel):
    passenger_name: str
    age: int
    contact_number: str
    origin: str
    destination: str
    flight_number: int
    flight_date: str
    seat_preference: str

    @field_validator("passenger_name")
    @classmethod
    def validate_passenger_name(cls, value):
        value = value.strip()

        if len(value) < 2 or len(value) > 50:
            raise ValueError("Passenger name must be between 2 and 50 characters long")

        for character in value:
            if not (character.isalpha() or character == " " or character == "-" or character == "'"):
                raise ValueError("Passenger name can only contain letters, spaces, hyphens, and apostrophes")

        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 0 or value > 120:
            raise ValueError("Age must be between 0 and 120")

        return value

    @field_validator("contact_number")
    @classmethod
    def validate_contact_number(cls, value):
        value = value.strip()

        digits_only = value
        if digits_only.startswith("+"):
            digits_only = digits_only[1:]

        if not digits_only.isdigit():
            raise ValueError("Contact number must contain only digits, with an optional leading +")

        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError("Contact number must be between 7 and 15 digits long")

        return value

    @field_validator("origin", "destination")
    @classmethod
    def validate_city_name(cls, value):
        value = value.strip()

        if len(value) < 2 or len(value) > 50:
            raise ValueError("City name must be between 2 and 50 characters long")

        for character in value:
            if not (character.isalpha() or character == " "):
                raise ValueError("City name can only contain letters and spaces")

        return value

    @field_validator("flight_number")
    @classmethod
    def validate_flight_number(cls, value):
        if value < 1 or value > 9999:
            raise ValueError("Flight number must be between 1 and 9999")

        return value

    @field_validator("flight_date")
    @classmethod
    def validate_flight_date(cls, value):
        value = value.strip()

        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Flight date must be in YYYY-MM-DD format")

        today = datetime.now().date()
        if parsed_date.date() < today:
            raise ValueError("Flight date cannot be in the past")

        return value

    @field_validator("seat_preference")
    @classmethod
    def validate_seat_preference(cls, value):
        value = value.strip().capitalize()

        if value not in VALID_SEAT_PREFERENCES:
            raise ValueError("Seat preference must be one of: " + ", ".join(VALID_SEAT_PREFERENCES))

        return value

    @model_validator(mode="after")
    def validate_origin_not_destination(self):
        if self.origin.lower() == self.destination.lower():
            raise ValueError("Origin and destination cannot be the same city")

        return self


class BookingResponse(BaseModel):
    message: str
    booking_reference: str
    passenger_name: str
    flight_number: int
    origin: str
    destination: str
    flight_date: str
    seat_preference: str