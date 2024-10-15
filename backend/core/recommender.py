# backend/core/recommender.py

from sklearn.preprocessing import MinMaxScaler
from pykeen.predict import predict_target
from .utils import create_node_label, UNKNOWN_PLACEHOLDER
from .data_loading import recipes_df, recipes
from .model import result
import pandas as pd
import ast

# Function to map user input to criteria
def map_user_input_to_criteria(meal_type, calories, carbs, protein, fat, diet_type, region, cook_time, ingredients, weights, country):
    criteria = []

    if meal_type:
        meal_type_entity = create_node_label(meal_type)
        criteria.append((meal_type_entity, 'isForMealType', weights.get('meal_type', 1.0)))

    if diet_type:
        diet_type_entity = create_node_label(diet_type)
        criteria.append((diet_type_entity, 'hasDietType', weights.get('diet_type', 1.0)))

    if region:
        region_entity = create_node_label(region)
        criteria.append((region_entity, 'isFromRegion', weights.get('region', 1.0)))

    if cook_time:
        cook_time_entity = create_node_label(cook_time)
        criteria.append((cook_time_entity, 'needTimeToCook', weights.get('cook_time', 1.0)))

    if country:
        country_entity = create_node_label(country)
        criteria.append((country_entity, 'isFromCountry', weights.get('country', 1.0)))

    if calories:
        calories_level = f'{calories.lower()}_calorie'
        criteria.append((calories_level, 'HasCalorieLevel', weights.get('calories', 1.0)))

    if carbs:
        carbs_level = f'{carbs.lower()}_carb'
        criteria.append((carbs_level, 'HasCarbLevel', weights.get('carbs', 1.0)))

    if protein:
        protein_level = f'{protein.lower()}_protein'
        criteria.append((protein_level, 'HasProteinLevel', weights.get('protein', 1.0)))

    if fat:
        fat_level = f'{fat.lower()}_fat'
        criteria.append((fat_level, 'HasFatLevel', weights.get('fat', 1.0)))

    if ingredients:
        for ingredient in ingredients:
            ingredient_entity = create_node_label(ingredient)
            criteria.append((ingredient_entity, 'contains', weights.get('ingredients', 1.0)))

    return criteria

# Function to normalize a column of scores
def normalize_scores(predictions):
    scaler = MinMaxScaler(feature_range=(0, 1))
    predictions['normalized_score'] = scaler.fit_transform(predictions[['score']])
    return predictions

# Function to get matching recipes based on criteria
def get_matching_recipes(criteria):
    all_predictions = []

    for tail_entity, relation, weight in criteria:
        # Get the predictions for the current criterion
        predicted_heads = predict_target(
            model=result.model,
            relation=relation,
            tail=tail_entity,
            triples_factory=result.training,  # Use the training triples factory
        ).df

        # Normalize the scores to ensure a balanced result
        predicted_heads = normalize_scores(predicted_heads)

        # Apply the weight to the normalized score
        predicted_heads['weighted_score'] = predicted_heads['normalized_score'] * weight
        all_predictions.append(predicted_heads[['head_label', 'weighted_score']])

    if not all_predictions:
        return []

    # Intersect predictions for multiple criteria (strict matching)
    merged_predictions = all_predictions[0][['head_label', 'weighted_score']]

    for preds in all_predictions[1:]:
        # Use inner join to keep only common results
        merged_predictions = merged_predictions.merge(
            preds[['head_label', 'weighted_score']],
            on='head_label',
            how='inner',
            suffixes=('', '_y')
        )

        # Sum weighted scores
        if 'weighted_score_y' in merged_predictions.columns:
            merged_predictions['weighted_score'] += merged_predictions['weighted_score_y']
            merged_predictions = merged_predictions.drop(columns=['weighted_score_y'])

    # Filter predictions to include only valid recipe names from the dataset
    valid_recipe_names = set(recipes_df['Name'])
    final_predictions_filtered = merged_predictions[merged_predictions['head_label'].isin(valid_recipe_names)]

    # Sort by combined weighted score
    final_predictions_sorted = final_predictions_filtered.sort_values(by='weighted_score', ascending=False)

    recipe_names = final_predictions_sorted['head_label'].tolist()

    return recipe_names

# Function to fetch and format recipe information
def fetch_recipe_info(recipe_name):
    # Check if the recipe exists in the dataframe
    matched_recipes = recipes_df[recipes_df['Name'] == recipe_name]
    if matched_recipes.empty:
        return None

    info = matched_recipes.iloc[0]
    # Process fields
    meal_type = [mt.replace('_', ' ').title() for mt in info.get('meal_type', '').split(',') if mt]
    diet_type = [dt.replace('_', ' ').title() for dt in info.get('Diet_Types', '').split(',') if dt]
    health_type = [ht.replace('_', ' ').title() for ht in info.get('Healthy_Type', '').split(',') if ht]
    region = [rc.replace('_', ' ').title() for rc in info.get('RegionPart', '').split(',') if rc]
    country = [cc.replace('_', ' ').title() for cc in info.get('CountryPart', '').split(',') if cc]
    cook_time = info.get('cook_time', '').replace('_', ' ').title()
    ingredients = info.get('ScrapedIngredients', '').split(',')
    instructions = info.get('RecipeInstructions', '')
    # Nutrition facts
    nutrition_facts = {
        'Calories': f"{info.get('Calories', 'N/A')} kcal",
        'FatContent': f"{info.get('FatContent', 'N/A')} g",
        'CarbohydrateContent': f"{info.get('CarbohydrateContent', 'N/A')} g",
        'ProteinContent': f"{info.get('ProteinContent', 'N/A')} g",
        'FiberContent': f"{info.get('FiberContent', 'N/A')} g",
        'SugarContent': f"{info.get('SugarContent', 'N/A')} g",
        'SodiumContent': f"{info.get('SodiumContent', 'N/A')} mg",
        'CholesterolContent': f"{info.get('CholesterolContent', 'N/A')} mg",
        'SaturatedFatContent': f"{info.get('SaturatedFatContent', 'N/A')} g",
    }
    # Images
    images = []
    if info.get('Images') and info.get('Images') != '[]':
        try:
            image_urls_str = info['Images']
            # Parse the string as a list of lists
            image_urls_nested = ast.literal_eval(image_urls_str)
            # Flatten the nested list
            images = [url for sublist in image_urls_nested for url in (sublist if isinstance(sublist, list) else [sublist]) if url]
        except Exception as e:
            images = []

    recipe_info = {
        "name": info['Name'].replace('_', ' ').title(),
        "description": info.get('Description', 'N/A'),
        "meal_type": meal_type,
        "diet_type": diet_type,
        "health_type": health_type,
        "region": region,
        "country": country,
        "cook_time": cook_time,
        "ingredients": ingredients,
        "instructions": instructions,
        "nutrition_facts": nutrition_facts,
        "images": images
    }
    return recipe_info
