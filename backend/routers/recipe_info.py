# backend/routers/recipe_info.py

from fastapi import APIRouter, HTTPException
from models.schemas import RecipeInfo
from core.recommender import fetch_recipe_info

router = APIRouter()

@router.get("/recipe/{recipe_name}", response_model=RecipeInfo)
def get_recipe_info(recipe_name: str):
    # Fetch and format recipe information
    info_dict = fetch_recipe_info(recipe_name)
    if info_dict is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Convert info_dict to RecipeInfo model
    recipe_info = RecipeInfo(**info_dict)
    return recipe_info
