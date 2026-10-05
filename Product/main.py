from typing import List, Optional
from fastapi import FastAPI, Query

from src.models import Product
from src import services


app = FastAPI(
    title= "Product Search API",
    description="Search a product catalog by name, category and price range"
)


@app.get("/products/search", response_model=List[Product], tags=["Products"])
def search_products(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=100,
        description="Case-insensitive substring match on product name",
        examples=["mouse"],
    ),
    category: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        description = ("Case-insensitive exact match, known categories: " + ", ".join(services.get_all_categories())),
        examples=["Electronics"],            
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Minimum price (inclusive) must be >= 0.",
        examples=[10.0],
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Maximum pric (inclusive), must be >= 0",
        examples=[200.0],
    ),
    in_stock: Optional[bool] = Query(
        None,
        description="Filter by stock status"
    ),
) -> List[Product]:

    return services.search_products(
        name=name,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
    )


@app.get("/products/categories", response_model=List[str], tags=["Products"])
def list_categories() -> List[str]:
    return services.get_all_categories()


@app.get("/", include_in_schema=False)
def root():
    return{"message": "Product Search API"}
