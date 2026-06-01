import streamlit as st
import pickle

from recommender import recommend

movies = pickle.load(
    open("models/movies.pkl", "rb")
)

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬"
)

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Choose Movie",
    movies["title"].values
)

if st.button("Recommend"):

    recommendations = recommend(
        selected_movie
    )

    st.subheader(
        "Recommended Movies"
    )

    for movie in recommendations:

        st.write(movie)