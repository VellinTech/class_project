from src.models import RegisterRequest, LoginRequest
import hashlib
import os


registered_users = {}

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)

    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    salt_hex = salt.hex()

    return hashed_password, salt_hex


def verify_password(password, stored_hash, stored_salt_hex):
    salt = bytes.fromhex(stored_salt_hex)
    hashed_password, _ = hash_password(password, salt)
    return hashed_password == stored_hash


def register_user(request: RegisterRequest):
    # Returns a tuple: (success, message, password_hash)
    # success is True/False, message explains the outcome.
    # password_hash is None when the registration is not successful.

    if request.username in registered_users:
        return False, "Username is already taken", None

    for existing_user in registered_users.values():
        if existing_user["email"] == request.email:
            return False, "Email is already registered", None

    hashed_password, salt_hex = hash_password(request.password)

    registered_users[request.username] = {
        "email": request.email,
        "password_hash": hashed_password,
        "salt": salt_hex,
    }

    return True, "User registered successfully", hashed_password


def login_user(request: LoginRequest):
    # Returns a tuple: (success, message)

    if request.username not in registered_users:
        return False, "Invalid username or password"

    stored_user = registered_users[request.username]

    if not verify_password(request.password, stored_user["password_hash"], stored_user["salt"]):
        return False, "Invalid username or password"

    return True, "Login successful"