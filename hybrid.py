import pandas as pd
import pickle

from surprise import Dataset
from surprise import Reader
from surprise import SVD

# LOAD DATA
movies = pd.read_csv(
    "data/movies.csv"
)

ratings = pd.read_csv(
    "data/ratings.csv"
)

# SURPRISE FORMAT
reader = Reader(
    rating_scale=(0.5, 5)
)

data = Dataset.load_from_df(
    ratings[
        ["userId", "movieId", "rating"]
    ],
    reader
)

# BUILD TRAINSET
trainset = data.build_full_trainset()

# TRAIN MODEL
model = SVD()

model.fit(trainset)

# SAVE MODEL
pickle.dump(
    model,
    open("models/collab_model.pkl", "wb")
)

print("Collaborative filtering model trained!")