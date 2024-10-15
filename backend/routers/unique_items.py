# backend/routers/unique_items.py

from fastapi import APIRouter
from typing import List
from core.data_loading import unique_ingredients, unique_regions, unique_countries

router = APIRouter()

@router.get("/unique_ingredients", response_model=List[str])
def get_unique_ingredients_endpoint():
    return unique_ingredients

@router.get("/unique_regions", response_model=List[str])
def get_unique_regions_endpoint():
    return unique_regions

@router.get("/unique_countries", response_model=List[str])
def get_unique_countries_endpoint():
    return unique_countries
