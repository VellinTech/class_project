from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float = Field(..., ge=0, description="Price in USD")
    in_stock: bool = True

