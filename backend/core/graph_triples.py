# backend/core/graph_triples.py

import numpy as np
import networkx as nx
import pickle
import pandas as pd
from .utils import UNKNOWN_PLACEHOLDER

def create_graph_and_triples(recipes):
    G = nx.Graph()
    triples = []

    for recipe, details in recipes.items():
        G.add_node(recipe, type='recipe')
        for relation_type, elements in details.items():
            if isinstance(elements, list):  # Handle lists
                for element in elements:
                    if element != UNKNOWN_PLACEHOLDER and element != '':
                        if relation_type == 'healthy_types':
                            # Generalize the relation to HasProteinLevel, HasCarbLevel, etc.
                            if 'protein' in element:
                                relation = 'HasProteinLevel'
                            elif 'carb' in element:
                                relation = 'HasCarbLevel'
                            elif 'fat' in element and 'saturated' not in element:
                                relation = 'HasFatLevel'
                            elif 'saturated_fat' in element:
                                relation = 'HasSaturatedFatLevel'
                            elif 'calorie' in element:
                                relation = 'HasCalorieLevel'
                            elif 'sodium' in element:
                                relation = 'HasSodiumLevel'
                            elif 'sugar' in element:
                                relation = 'HasSugarLevel'
                            elif 'fiber' in element:
                                relation = 'HasFiberLevel'
                            elif 'cholesterol' in element:
                                relation = 'HasCholesterolLevel'
                            else:
                                relation = 'HasHealthAttribute'  # For other health attributes
                            G.add_node(element, type=relation)
                        else:
                            G.add_node(element, type=relation_type)
                            relation = {
                                'ingredients': 'contains',
                                'diet_types': 'hasDietType',
                                'meal_type': 'isForMealType',
                                'cook_time': 'needTimeToCook',
                                'regions': 'isFromRegion',
                                'countries': 'isFromCountry',
                            }.get(relation_type, 'hasAttribute')
                        G.add_edge(recipe, element, relation=relation)
                        triples.append((recipe, relation, element))
            else:  # Handle single elements like cook_time
                element = elements
                if element != UNKNOWN_PLACEHOLDER and element != '':
                    G.add_node(element, type=relation_type)
                    relation = {
                        'cook_time': 'needTimeToCook',
                        'ingredients': 'contains',
                        'diet_types': 'hasDietType',
                        'meal_type': 'isForMealType',
                        'regions': 'isFromRegion',
                        'countries': 'isFromCountry',
                    }.get(relation_type, 'hasAttribute')
                    G.add_edge(recipe, element, relation=relation)
                    triples.append((recipe, relation, element))

    return G, np.array(triples, dtype=str)

# Function to save triples to CSV
def save_triples(triples_array, file_path):
    # Convert the triples array into a pandas DataFrame
    triples_df = pd.DataFrame(triples_array, columns=['Head', 'Relation', 'Tail'])
    # Save triples DataFrame to CSV
    triples_df.to_csv(file_path, index=False)

# Function to save the graph
def save_graph(G, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(G, f)
