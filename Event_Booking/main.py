from fastapi import FastAPI

from src.models import CourseRegistrationRequest, CourseRegistrationResponse
from src import services


app = FastAPI(
    title="Student Course Registration API",
    description="Register students for university courses with request validation.",
    version="1.0.0",
)


@app.post(
    "/registrations",
    response_model=CourseRegistrationResponse,
    tags=["Course Registration"]
)
def register_course(
    registration: CourseRegistrationRequest
) -> CourseRegistrationResponse:

    return services.register_course(registration)


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Student Course Registration API - visit /docs for Swagger UI"
    }