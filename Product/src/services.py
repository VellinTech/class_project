from typing import List, Annotated, Optional
from fastapi import HTTPException
from src.models import Product


# In-memory catalog (swap for a real DB later)

PRODUCTS: List[Product] = [
    Product(id=1,  name="Wireless Mouse",        category="Electronics", price=19.99,  in_stock=True),
    Product(id=2,  name="Mechanical Keyboard",    category="Electronics", price=79.99,  in_stock=True),
    Product(id=3,  name="USB-C Hub",              category="Electronics", price=34.50,  in_stock=False),
    Product(id=4,  name="Noise Cancelling Headphones", category="Electronics", price=199.99, in_stock=True),
    Product(id=5,  name="Running Shoes",          category="Footwear",    price=89.00,  in_stock=True),
    Product(id=6,  name="Leather Boots",          category="Footwear",    price=145.00, in_stock=True),
    Product(id=7,  name="Yoga Mat",                category="Fitness",     price=24.99,  in_stock=True),
    Product(id=8,  name="Adjustable Dumbbell Set", category="Fitness",     price=249.99, in_stock=False),
    Product(id=9,  name="Ceramic Coffee Mug",      category="Kitchen",     price=12.50,  in_stock=True),
    Product(id=10, name="Stainless Steel Kettle",  category="Kitchen",     price=44.00,  in_stock=True),
    Product(id=11, name="Office Chair",            category="Furniture",   price=159.00, in_stock=True),
    Product(id=12, name="Standing Desk",           category="Furniture",   price=349.00, in_stock=True),
]


def get_all_categories() -> List[str]:
    return sorted({p.category for p in PRODUCTS})


def search_products(
    name: Annotated[Optional[str], "Case-insensitive substring match on product name"] = None,
    category: Annotated[Optional[str], "Case-insensitive exact match on category"] = None,
    min_price: Annotated[Optional[float], "Minimum price, inclusive"] = None,
    max_price: Annotated[Optional[float], "Maximum price, inclusive"] = None,
    in_stock: Annotated[Optional[bool], "Filter by stock status"] = None,
) -> List[Product]:

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price.",
        )

    results = PRODUCTS

    if name:
        needle = name.lower()
        results = [p for p in results if needle in p.name.lower()]

    if category:
        results = [p for p in results if p.category.lower() == category.lower()]

    if min_price is not None:
        results = [p for p in results if p.price >= min_price]

    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    if in_stock is not None:
        results = [p for p in results if p.in_stock == in_stock]

    return results