# backend/routers/recommend.py

from fastapi import APIRouter
from typing import List
from models.schemas import RecommendationRequest
from core.recommender import map_user_input_to_criteria, get_matching_recipes

router = APIRouter()

@router.post("/recommend", response_model=List[str])
def recommend_recipes(request: RecommendationRequest):
    # Map user input to criteria
    criteria = map_user_input_to_criteria(
        request.meal_type,
        request.calories,
        request.carbs,
        request.protein,
        request.fat,
        request.diet_type,
        request.region,
        request.cook_time,
        request.ingredients,
        request.weights,
        request.country
    )

    if criteria:
        matching_recipes = get_matching_recipes(criteria)
        return matching_recipes
    else:
        return []
