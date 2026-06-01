import requests

API_KEY = "aa5f2c88ee538bd9ea1492b75ad670b8"


def get_trending_movies():

    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"

    response = requests.get(url)

    data = response.json()

    movies = []

    posters = []

    for movie in data["results"][:5]:

        movies.append(movie["title"])

        posters.append(
            "https://image.tmdb.org/t/p/w500"
            + movie["poster_path"]
        )

    return movies, posters