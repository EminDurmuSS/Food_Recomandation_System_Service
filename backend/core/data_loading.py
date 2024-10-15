# backend/core/data_loading.py

import pandas as pd
import pickle
import os

# Define file paths
processed_data_path = '/app/FastAPI/data/processed_recipes_df.csv'
unique_regions_path = '/app/FastAPI/data/unique_regions.pkl'
unique_countries_path = '/app/FastAPI/data/unique_countries.pkl'
unique_ingredients_path = '/app/FastAPI/data/unique_ingredients.pkl'
recipes_dict_path = '/app/FastAPI/data/recipes_dict.pkl'
graph_file_path = '/app/FastAPI/data/graph.pkl'

# Load processed recipes DataFrame
def load_processed_recipes_df():
    if os.path.exists(processed_data_path):
        df = pd.read_csv(processed_data_path)
        return df
    else:
        raise FileNotFoundError(f"Processed recipes DataFrame not found at {processed_data_path}")

# Load unique regions
def load_unique_regions():
    if os.path.exists(unique_regions_path):
        with open(unique_regions_path, 'rb') as f:
            unique_regions = pickle.load(f)
        return unique_regions
    else:
        raise FileNotFoundError(f"Unique regions file not found at {unique_regions_path}")

# Load unique countries
def load_unique_countries():
    if os.path.exists(unique_countries_path):
        with open(unique_countries_path, 'rb') as f:
            unique_countries = pickle.load(f)
        return unique_countries
    else:
        raise FileNotFoundError(f"Unique countries file not found at {unique_countries_path}")

# Load unique ingredients
def load_unique_ingredients():
    if os.path.exists(unique_ingredients_path):
        with open(unique_ingredients_path, 'rb') as f:
            unique_ingredients = pickle.load(f)
        return unique_ingredients
    else:
        raise FileNotFoundError(f"Unique ingredients file not found at {unique_ingredients_path}")

# Load recipes dictionary
def load_recipes_dict():
    if os.path.exists(recipes_dict_path):
        with open(recipes_dict_path, 'rb') as f:
            recipes = pickle.load(f)
        return recipes
    else:
        raise FileNotFoundError(f"Recipes dictionary file not found at {recipes_dict_path}")

# Optionally, load the graph
def load_graph():
    if os.path.exists(graph_file_path):
        with open(graph_file_path, 'rb') as f:
            G = pickle.load(f)
        return G
    else:
        raise FileNotFoundError(f"Graph file not found at {graph_file_path}")

# Load all data
recipes_df = load_processed_recipes_df()
unique_regions = load_unique_regions()
unique_countries = load_unique_countries()
unique_ingredients = load_unique_ingredients()
recipes = load_recipes_dict()
# G = load_graph()  # Uncomment if you need the graph
