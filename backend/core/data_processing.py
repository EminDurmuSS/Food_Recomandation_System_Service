# backend/core/data_processing.py

import os
import pandas as pd
import numpy as np
import ast
import pickle
from .utils import create_node_label, UNKNOWN_PLACEHOLDER
from .graph_triples import create_graph_and_triples, save_triples, save_graph

def process_list_column(x):
    if pd.isna(x) or x == '':
        return ''
    # Split the string on commas
    items = [item.strip() for item in x.split(',')]
    return ','.join([create_node_label(item) for item in items])

# Function to preprocess the data
def preprocess_data(file_path):
    # Load data
    df = pd.read_csv(file_path)
    df = df.drop_duplicates(subset='Name', keep='first')  # Ensure unique recipes
    df = df.reset_index(drop=True)
    
    # Process the dataframe and clean labels
    df['Name'] = df['Name'].apply(create_node_label)
        
    list_columns = ['RecipeIngredientParts', 'Healthy_Type', 'meal_type', 'Diet_Types', 'RegionPart', 'CountryPart', 'Best_foodentityname']
    for col in list_columns:
        df[col] = df[col].apply(process_list_column)
    
    df['cook_time'] = df['cook_time'].apply(create_node_label)
    return df

# Function to get unique regions from RegionPart column
def get_unique_regions(df):
    regions_set = set()
    for regions in df['RegionPart']:
        if regions:
            for region in regions.split(','):
                regions_set.add(region.strip())
    unique_regions = [''] + sorted(regions_set)
    return unique_regions

# Function to get unique countries from CountryPart column
def get_unique_countries(df):
    countries_set = set()
    for countries in df['CountryPart']:
        if countries:
            for country in countries.split(','):
                if country:
                    countries_set.add(country.strip())
    unique_countries = [''] + sorted(countries_set)
    return unique_countries

# Function to get unique ingredients from Best_foodentityname column
def get_unique_ingredients(df):
    ingredients_set = set()
    for ingredients in df['Best_foodentityname']:
        if ingredients:
            for ingredient in ingredients.split(','):
                ingredients_set.add(ingredient.strip())
    unique_ingredients = sorted(ingredients_set)
    return unique_ingredients

# Function to create the recipes dictionary
def create_recipes_dict(df):
    recipes = {}
    for _, row in df.iterrows():
        recipe_name = create_node_label(row['Name'])
        
        # Process ingredients
        Best_foodentityname = [
            create_node_label(ing.strip()) 
            for ing in row['Best_foodentityname'].split(',') 
            if ing.strip() != ''
        ]
        
        # Process healthy types
        healthy_types = [
            create_node_label(ht.strip()) 
            for ht in row['Healthy_Type'].split(',') 
            if ht.strip() != ''
        ]
        
        # Process meal types
        meal_types = [
            create_node_label(mt.strip()) 
            for mt in row['meal_type'].split(',') 
            if mt.strip() != ''
        ]
        
        # Process cook_time
        cook_time = create_node_label(row['cook_time'])
        
        # Process diet types
        diet_types = [
            create_node_label(dt.strip()) 
            for dt in row['Diet_Types'].split(',')
        ] if row['Diet_Types'] != UNKNOWN_PLACEHOLDER else [UNKNOWN_PLACEHOLDER]
        
        # Process regions
        regions = [
            create_node_label(rc.strip()) 
            for rc in row['RegionPart'].split(',') 
            if rc.strip() != ''
        ]
        
        # Process countries
        countries = [
            create_node_label(cc.strip()) 
            for cc in row['CountryPart'].split(',') 
            if cc.strip() != ''
        ]
        
        # Construct the recipe dictionary
        recipes[recipe_name] = {
            "ingredients": Best_foodentityname,
            "diet_types": diet_types,
            "meal_type": meal_types,
            "cook_time": cook_time,
            "regions": regions,
            "countries": countries,
            "healthy_types": healthy_types,
        }
    return recipes

# Adjust the file paths as needed
file_path = '/app/FoodRecomandationSystem/data/dataFullLargerRegionAndCountry.csv'
triples_file_path = '/app/FoodRecomandationSystem/data/triples_df.csv'
graph_file_path = '/app/FoodRecomandationSystem/data/graph.pkl'

# Preprocess data
recipes_df = preprocess_data(file_path)

# Get unique regions, countries, ingredients
unique_regions = get_unique_regions(recipes_df)
unique_countries = get_unique_countries(recipes_df)
unique_ingredients = get_unique_ingredients(recipes_df)

# Create recipes dictionary
recipes = create_recipes_dict(recipes_df)

# Create the graph and triples
G, triples_array = create_graph_and_triples(recipes)

# Save triples DataFrame to CSV
save_triples(triples_array, triples_file_path)

# Save the graph
save_graph(G, graph_file_path)

# Save processed recipes_df to a CSV file
recipes_df.to_csv('/app/FoodRecomandationSystem/data/processed_recipes_df.csv', index=False)

# Save unique regions, countries, ingredients
with open('/app/FoodRecomandationSystem/data/unique_regions.pkl', 'wb') as f:
    pickle.dump(unique_regions, f)

with open('/app/FoodRecomandationSystem/data/unique_countries.pkl', 'wb') as f:
    pickle.dump(unique_countries, f)

with open('/app/FoodRecomandationSystem/data/unique_ingredients.pkl', 'wb') as f:
    pickle.dump(unique_ingredients, f)

# Save recipes dictionary
with open('/app/FoodRecomandationSystem/data/recipes_dict.pkl', 'wb') as f:
    pickle.dump(recipes, f)

print("Data preprocessing completed.")
