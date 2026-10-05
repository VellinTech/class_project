from fastapi import FastAPI, HTTPException

from src.models import RegistrationRequest, RegistrationResponse
from src.services import register_student


app = FastAPI(title="Student Event Registration API")


@app.post(
    "/registrations",
    response_model=RegistrationResponse,
    status_code=201
)
def create_registration(request: RegistrationRequest):

    success, message, registration_id = register_student(request)

    if not success:
        raise HTTPException(
            status_code=400,
            detail=message
        )

    return RegistrationResponse(
        message=message,
        registration_id=registration_id,
        student_name=request.student_name,
        matric_number=request.matric_number,
        event_name=request.event_name,
        department=request.department,
        registration_date=request.registration_date,
    )