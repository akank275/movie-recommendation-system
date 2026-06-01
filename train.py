import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data/movies.csv")

movies["genres"] = movies["genres"].fillna("")

tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(
    movies["genres"]
)

similarity = cosine_similarity(
    tfidf_matrix
)

pickle.dump(
    movies,
    open("models/movies.pkl", "wb")
)

pickle.dump(
    similarity,
    open("models/similarity.pkl", "wb")
)

print("Model trained successfully!")