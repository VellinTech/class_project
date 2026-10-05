from pydantic import BaseModel, field_validator
import re


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        value = value.strip()

        if len(value) < 3 or len(value) > 20:
            raise ValueError("Username must be between 3 and 20 characters long")

        if not re.match("^[a-zA-Z0-9_]+$", value):
            raise ValueError("Username can only contain letters, numbers, and underscores")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip()

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, value):
            raise ValueError("Email format is invalid")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False

        for character in value:
            if character.isupper():
                has_upper = True
            elif character.islower():
                has_lower = True
            elif character.isdigit():
                has_digit = True
            elif character in "!@#$%^&*()-_=+[]{};:,.<>?":
                has_special = True

        if not has_upper:
            raise ValueError("Password must contain at least one uppercase letter")

        if not has_lower:
            raise ValueError("Password must contain at least one lowercase letter")

        if not has_digit:
            raise ValueError("Password must contain at least one digit")

        if not has_special:
            raise ValueError("Password must contain at least one special character")

        return value


class RegisterResponse(BaseModel):
    message: str
    username: str
    email: str
    password_hash: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str