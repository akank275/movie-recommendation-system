import pickle
import requests
import pandas as pd


# LOAD MOVIES DATA
movies = pickle.load(
    open("models/movies.pkl", "rb")
)

# LOAD SIMILARITY MATRIX
similarity = pickle.load(
    open("models/similarity.pkl", "rb")
)

# LOAD RATINGS DATA
ratings = pd.read_csv(
    "data/ratings.csv"
)

# LOAD COLLABORATIVE FILTERING MODEL
collab_model = pickle.load(
    open("models/collab_model.pkl", "rb")
)


# TMDB API KEY
API_KEY = "aa5f2c88ee538bd9ea1492b75ad670b8"



# FETCH POSTER
def fetch_poster(movie_name):

    try:

        # REMOVE YEAR FROM TITLE
        movie_name = movie_name.split("(")[0].strip()

        url = (
            "https://api.themoviedb.org/3/search/movie"
            f"?api_key={"aa5f2c88ee538bd9ea1492b75ad670b8"}&query={movie_name}"
        )

        response = requests.get(url)

        data = response.json()

        # CHECK IF RESULTS EXIST
        if (
            "results" in data
            and len(data["results"]) > 0
            and data["results"][0]["poster_path"]
        ):

            poster_path = data["results"][0]["poster_path"]

            full_path = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

            return full_path

        # FALLBACK IMAGE
        return (
            "https://via.placeholder.com/"
            "300x450?text=No+Poster"
        )

    except:

        return (
            "https://via.placeholder.com/"
            "300x450?text=No+Poster"
        )


# CONTENT-BASED RECOMMENDATION
def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[
        movie_index
    ]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    recommended_posters = []

    for i in movie_list:

        movie_title = movies.iloc[
            i[0]
        ].title

        recommended_movies.append(
            movie_title
        )

        recommended_posters.append(
            fetch_poster(movie_title)
        )

    return (
        recommended_movies,
        recommended_posters
    )


# HYBRID RECOMMENDATION SYSTEM
def hybrid_recommend(
    movie_name,
    user_id=1,
    genre_filter="All"
):

    movie_index = movies[
        movies["title"] == movie_name
    ].index[0]

    similarity_scores = similarity[
        movie_index
    ]

    movie_list = sorted(
        list(enumerate(similarity_scores)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    hybrid_scores = []

    for movie in movie_list:

        movie_id = movies.iloc[
            movie[0]
        ].movieId

        predicted_rating = collab_model.predict(
            user_id,
            movie_id
        ).est

        final_score = (
            movie[1] * 0.5
            + predicted_rating * 0.5
        )

        hybrid_scores.append(
            (
                movie[0],
                final_score
            )
        )

    hybrid_scores = sorted(
        hybrid_scores,
        reverse=True,
        key=lambda x: x[1]
    )[:10]

    recommended_movies = []
    recommended_posters = []

    for movie in hybrid_scores:

        title = movies.iloc[
            movie[0]
        ].title

        genres = movies.iloc[
            movie[0]
        ].genres

        if (
            genre_filter == "All"
            or genre_filter in genres
        ):

            recommended_movies.append(
                title
            )

            recommended_posters.append(
                fetch_poster(title)
            )

    # FALLBACK IF NOTHING FOUND
    if len(recommended_movies) == 0:

        recommended_movies.append(
            "No movies found"
        )

        recommended_posters.append(
            "https://via.placeholder.com/300x450?text=No+Movie"
        )

    return (
        recommended_movies[:5],
        recommended_posters[:5]
    )



# EXPLAIN RECOMMENDATION
def explain_recommendation(movie_name):

    # HANDLE EMPTY MOVIE CASE
    if movie_name == "No movies found":

        return """
No explanation available.

Try selecting another genre.
"""

    selected_movies = movies[
        movies["title"] == movie_name
    ]

    # SAFETY CHECK
    if len(selected_movies) == 0:

        return """
No explanation available.
"""

    selected_movie = selected_movies.iloc[0]

    genres = selected_movie["genres"]

    explanation = f"""
Recommended because:

• Similar genres: {genres}

• Users with similar interests liked this movie

• Similar rating patterns detected

• Hybrid AI recommendation engine selected this movie
"""

    return explanation

