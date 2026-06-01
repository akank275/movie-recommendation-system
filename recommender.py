import pickle

movies = pickle.load(
    open("models/movies.pkl", "rb")
)

similarity = pickle.load(
    open("models/similarity.pkl", "rb")
)

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

    recommendations = []

    for i in movie_list:

        recommendations.append(
            movies.iloc[i[0]].title
        )

    return recommendations