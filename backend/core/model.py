# backend/core/model.py

import os
import pickle
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
import pandas as pd

# Load triples and create a TriplesFactory
triples_df = pd.read_csv('/app/FoodRecomandationSystem/data/triples_df.csv')  # Adjusted file path
triples = triples_df[['Head', 'Relation', 'Tail']].values
triples_factory = TriplesFactory.from_labeled_triples(triples)

# Train the model using PyKEEN
def train_model(triples_factory):
    model_file = '/app/FoodRecomandationSystem/embedding/LargerDataQuatE_model.pkl'  # Adjusted file path
    if os.path.exists(model_file):
        # Load the existing model
        with open(model_file, 'rb') as f:
            result = pickle.load(f)
    else:
        # Train the model
        result = pipeline(
            model='QuatE',
            training=triples_factory,
            testing=triples_factory,
            validation=triples_factory,
            epochs=400,
            stopper='early',
        )
        # Save the model
        with open(model_file, 'wb') as f:
            pickle.dump(result, f)
    return result

# Load or train the model
result = train_model(triples_factory)

print("Train complated")