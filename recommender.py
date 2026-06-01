import pickle
import requests

movies = pickle.load(
    open("models/movies.pkl", "rb")
)

similarity = pickle.load(
    open("models/similarity.pkl", "rb")
)

API_KEY = "aa5f2c88ee538bd9ea1492b75ad670b8"


def fetch_poster(movie_name):

    # Remove year from movie title
    movie_name = movie_name.split("(")[0].strip()

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    response = requests.get(url)

    data = response.json()

    try:

        poster_path = data["results"][0]["poster_path"]

        full_path = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

        return full_path

    except:

        return "https://via.placeholder.com/300x450?text=No+Poster"


def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    recommended_posters = []

    for i in movie_list:

        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(
            movie_title
        )

        recommended_posters.append(
            fetch_poster(movie_title)
        )

    return recommended_movies, recommended_posters