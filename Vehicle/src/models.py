from pydantic import BaseModel, Field


class Vehicle(BaseModel):
    id: int
    make: str = Field(..., min_length=2, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1900, le=2030)
    price: float = Field(..., gt=0)


    