import pandas as pd
import plotly.express as px


# LOAD DATA
movies = pd.read_csv(
    "data/movies.csv"
)

ratings = pd.read_csv(
    "data/ratings.csv"
)


# GENRE ANALYSIS
genre_count = (
    movies["genres"]
    .str.split("|")
    .explode()
    .value_counts()
)


# MOST RATED MOVIES
movie_ratings = ratings.groupby(
    "movieId"
)["rating"].count().sort_values(
    ascending=False
).head(10)

top_movies = movies[
    movies["movieId"].isin(
        movie_ratings.index
    )
]


# GENRE CHART
def genre_chart():

    fig = px.bar(
        x=genre_count.index,
        y=genre_count.values,
        title="Top Movie Genres"
    )

    return fig


# RATING DISTRIBUTION
def rating_chart():

    fig = px.histogram(
        ratings,
        x="rating",
        nbins=10,
        title="Rating Distribution"
    )

    return fig


# TOP MOVIES CHART
def top_movies_chart():

    fig = px.bar(
        top_movies,
        x="title",
        y=movie_ratings.values,
        title="Most Rated Movies"
    )

    return fig

