from src.models import Vehicle

# sample vehicle inventory
vehicles = [
    Vehicle(
        id=1,
        make="Toyota",
        model="Camry",
        year=2022,
        price=25000
    ),
    Vehicle(
        id=2,
        make="Honda",
        model="Accord",
        year=2021,
        price=23000
    ),
    Vehicle(
        id=3,
        make="Toyota",
        model="Corolla",
        year=2023,
        price=22000
    ),
    Vehicle(
        id=4,
        make="BMW",
        model="X5",
        year=2022,
        price=60000
    ),
    Vehicle(
        id=5,
        make="Mercedes",
        model="C-Class",
        year=2023,
        price=55000
    ),
    Vehicle(
        id=6,
        make="Ford",
        model="Mustang",
        year=2021,
        price=40000
    ),
]


def get_vehicle_by_id(vehicle_id: int):
    for vehicle in vehicles:
        if vehicle.id == vehicle_id:
            return vehicle

    return None


def get_vehicles(
    make: str | None = None,
    model: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
):

    filtered_vehicles = vehicles

    if make:
        filtered_vehicles = [
            vehicle
            for vehicle in filtered_vehicles
            if vehicle.make.lower() == make.lower()
        ]

    if model:
        filtered_vehicles = [
            vehicle
            for vehicle in filtered_vehicles
            if vehicle.model.lower() == model.lower()
        ]

    if min_price is not None:
        filtered_vehicles = [
            vehicle
            for vehicle in filtered_vehicles
            if vehicle.price >= min_price
        ]

    if max_price is not None:
        filtered_vehicles = [
            vehicle
            for vehicle in filtered_vehicles
            if vehicle.price <= max_price
        ]

    return filtered_vehicles