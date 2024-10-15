# backend/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict

class RecommendationRequest(BaseModel):
    meal_type: Optional[str] = None
    calories: Optional[str] = None
    carbs: Optional[str] = None
    protein: Optional[str] = None
    fat: Optional[str] = None
    diet_type: Optional[str] = None
    region: Optional[str] = None
    cook_time: Optional[str] = None
    ingredients: Optional[List[str]] = None
    country: Optional[str] = None
    weights: Dict[str, float]

class RecipeInfo(BaseModel):
    name: str
    description: Optional[str] = None
    meal_type: List[str]
    diet_type: List[str]
    health_type: List[str]
    region: List[str]
    country: List[str]
    cook_time: str
    ingredients: List[str]
    instructions: str
    nutrition_facts: Dict[str, str]
    images: List[str]
