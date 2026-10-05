from fastapi import FastAPI, HTTPException
from src.models import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from src.services import register_user, login_user

app = FastAPI(title="User Registration API")


@app.post("/register", response_model=RegisterResponse, status_code=201)
def register(request: RegisterRequest):
    success, message, password_hash = register_user(request)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return RegisterResponse(
        message=message,
        username=request.username,
        email=request.email,
        password_hash=password_hash,
    )


@app.post("/login", response_model=LoginResponse, status_code=200)
def login(request: LoginRequest):
    success, message = login_user(request)

    if not success:
        raise HTTPException(status_code=401, detail=message)

    return LoginResponse(
        message=message,
        username=request.username,
    )