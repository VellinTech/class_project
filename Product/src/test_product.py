"""
Tests for the Product Search API.
Run: pytest test_main.py -v
"""

from fastapi.testclient import TestClient
from main import app
from services import PRODUCTS

client = TestClient(app)


def test_search_no_params_returns_everything():
    resp = client.get("/products/search")
    assert resp.status_code == 200
    assert len(resp.json()) == len(PRODUCTS)


def test_search_by_name_substring_case_insensitive():
    resp = client.get("/products/search", params={"name": "mouse"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Wireless Mouse"


def test_search_by_name_uppercase_still_matches():
    resp = client.get("/products/search", params={"name": "MOUSE"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_search_by_category_exact_match():
    resp = client.get("/products/search", params={"category": "Electronics"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 4
    assert all(p["category"] == "Electronics" for p in data)


def test_search_by_category_case_insensitive():
    resp = client.get("/products/search", params={"category": "electronics"})
    assert resp.status_code == 200
    assert len(resp.json()) == 4


def test_search_by_price_range():
    resp = client.get(
        "/products/search", params={"min_price": 20, "max_price": 100}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert all(20 <= p["price"] <= 100 for p in data)


def test_search_by_min_price_only():
    resp = client.get("/products/search", params={"min_price": 200})
    assert resp.status_code == 200
    data = resp.json()
    assert all(p["price"] >= 200 for p in data)


def test_search_by_max_price_only():
    resp = client.get("/products/search", params={"max_price": 20})
    assert resp.status_code == 200
    data = resp.json()
    assert all(p["price"] <= 20 for p in data)


def test_search_combined_name_category_and_price():
    resp = client.get(
        "/products/search",
        params={"category": "Electronics", "min_price": 0, "max_price": 50},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert all(p["category"] == "Electronics" and p["price"] <= 50 for p in data)


def test_search_in_stock_filter():
    resp = client.get("/products/search", params={"in_stock": True})
    assert resp.status_code == 200
    data = resp.json()
    assert all(p["in_stock"] is True for p in data)


def test_search_out_of_stock_filter():
    resp = client.get("/products/search", params={"in_stock": False})
    assert resp.status_code == 200
    data = resp.json()
    assert all(p["in_stock"] is False for p in data)


def test_search_no_match_returns_empty_list():
    resp = client.get("/products/search", params={"name": "nonexistent-item-xyz"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_invalid_price_range_returns_400():
    resp = client.get(
        "/products/search", params={"min_price": 500, "max_price": 10}
    )
    assert resp.status_code == 400
    assert "min_price" in resp.json()["detail"]


def test_negative_min_price_rejected_by_validation():
    resp = client.get("/products/search", params={"min_price": -5})
    assert resp.status_code == 422  # FastAPI/Pydantic validation error


def test_negative_max_price_rejected_by_validation():
    resp = client.get("/products/search", params={"max_price": -1})
    assert resp.status_code == 422


def test_empty_name_string_rejected_by_validation():
    resp = client.get("/products/search", params={"name": ""})
    assert resp.status_code == 422  # violates min_length=1


def test_too_long_name_rejected_by_validation():
    resp = client.get("/products/search", params={"name": "x" * 101})
    assert resp.status_code == 422  # violates max_length=100


def test_categories_endpoint_lists_known_categories():
    resp = client.get("/products/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert "Electronics" in data
    assert "Footwear" in data
    assert data == sorted(data)  # sorted alphabetically


def test_all_filters_together():
    resp = client.get(
        "/products/search",
        params={
            "name": "e",  # broad substring
            "category": "Furniture",
            "min_price": 100,
            "max_price": 400,
            "in_stock": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    for p in data:
        assert "e" in p["name"].lower()
        assert p["category"] == "Furniture"
        assert 100 <= p["price"] <= 400
        assert p["in_stock"] is True