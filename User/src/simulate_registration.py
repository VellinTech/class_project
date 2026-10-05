from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def run_test(description, username, email, password):
    response = client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    print(description)
    print("Status code:", response.status_code)
    print("Response body:", response.json())
    print("-" * 50)


# Successful registration
run_test(
    "Test 1: Valid registration",
    "pedri8",
    "pedri@barca.com",
    "Football1!",
)

# Username too short
run_test(
    "Test 2: Username too short",
    "ab",
    "lamine@barca.com",
    "Football1!",
)

# Invalid email format
run_test(
    "Test 3: Invalid email format",
    "haaland9",
    "haaland-at-city.com",
    "Football1!",
)

# Weak password (no uppercase, no special character)
run_test(
    "Test 4: Weak password",
    "messi10",
    "messi@intermiami.com",
    "football1",
)

# Duplicate username (registering pedri8 again from Test 1)
run_test(
    "Test 5: Duplicate username",
    "pedri8",
    "different_email@barca.com",
    "Football2!",
)