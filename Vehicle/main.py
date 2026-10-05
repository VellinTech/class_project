from fastapi import FastAPI, Path, Query, HTTPException

from src.models import Vehicle
from src.services import get_vehicle_by_id, get_vehicles


app = FastAPI(
    title="Vehicle Inventory API",
    description="API for managing and filtering vehicle inventory",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Vehicle Inventory API"
    }


@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
def get_vehicle(
    vehicle_id: int = Path(
        ...,
        gt=0,
        description="The ID of the vehicle"
    )
):
    """
    Get a specific vehicle by ID.
    """

    vehicle = get_vehicle_by_id(vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@app.get("/vehicles", response_model=list[Vehicle])
def list_vehicles(
    make: str | None = Query(
        default=None,
        min_length=2,
        max_length=50,
        description="Filter vehicles by make"
    ),

    model: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Filter vehicles by model"
    ),

    min_price: float | None = Query(
        default=None,
        ge=0,
        description="Minimum vehicle price"
    ),

    max_price: float | None = Query(
        default=None,
        ge=0,
        description="Maximum vehicle price"
    )
):
    """
    Get a list of vehicles with optional filters.
    """

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price"
        )

    return get_vehicles(
        make=make,
        model=model,
        min_price=min_price,
        max_price=max_price
    )