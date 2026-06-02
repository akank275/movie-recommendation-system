import streamlit as st
import pickle

from recommender import (
    recommend,
    hybrid_recommend,
    explain_recommendation
)

from trending import get_trending_movies

from auth import signup
from auth import login

from favorites import (
    add_favorite,
    get_favorites
)

from dashboard import (
    genre_chart,
    rating_chart,
    top_movies_chart
)


# PAGE CONFIG
st.set_page_config(
    page_title="Netflix Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# LOAD MOVIES
movies = pickle.load(
    open("models/movies.pkl", "rb")
)


# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "recommended_names" not in st.session_state:
    st.session_state.recommended_names = []

if "recommended_posters" not in st.session_state:
    st.session_state.recommended_posters = []


# TITLE
st.title("🎬 AI Movie Recommendation System")


# SIDEBAR MENU
menu = [
    "Home",
    "Login",
    "Signup",
    "Dashboard"
]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)


# HOME PAGE
if choice == "Home":

    st.subheader("🔥 Trending Movies")

    trend_names, trend_posters = get_trending_movies()

    t1, t2, t3, t4, t5 = st.columns(5)

    with t1:
        st.image(trend_posters[0])
        st.caption(trend_names[0])

    with t2:
        st.image(trend_posters[1])
        st.caption(trend_names[1])

    with t3:
        st.image(trend_posters[2])
        st.caption(trend_names[2])

    with t4:
        st.image(trend_posters[3])
        st.caption(trend_names[3])

    with t5:
        st.image(trend_posters[4])
        st.caption(trend_names[4])

    st.write(
        "Login to get personalized movie recommendations."
    )


# SIGNUP PAGE
elif choice == "Signup":

    st.subheader("Create New Account")

    new_user = st.text_input(
        "Username"
    )

    new_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Signup"):

        result = signup(
            new_user,
            new_password
        )

        if result:

            st.success(
                "Account created successfully!"
            )

        else:

            st.error(
                "Username already exists"
            )


# DASHBOARD PAGE
elif choice == "Dashboard":

    st.title("📊 Analytics Dashboard")

    st.subheader("🎭 Genre Distribution")

    st.plotly_chart(
        genre_chart(),
        use_container_width=True
    )

    st.subheader("⭐ Rating Distribution")

    st.plotly_chart(
        rating_chart(),
        use_container_width=True
    )

    st.subheader("🔥 Most Rated Movies")

    st.plotly_chart(
        top_movies_chart(),
        use_container_width=True
    )


# LOGIN PAGE
elif choice == "Login":

    # LOGIN FORM
    if not st.session_state.logged_in:

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            result = login(
                username,
                password
            )

            if result:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )

    # AFTER LOGIN
    else:

        username = st.session_state.username

        st.sidebar.success(
            f"Logged in as {username}"
        )

        # FAVORITES IN SIDEBAR
        st.sidebar.subheader(
            "❤️ Your Favorites"
        )

        favorites = get_favorites(
            username
        )

        for fav in favorites:

            st.sidebar.write(
                fav.movie
            )

        st.success(
            f"Welcome {username}"
        )

        # TRENDING MOVIES
        st.subheader("🔥 Trending Movies")

        trend_names, trend_posters = get_trending_movies()

        t1, t2, t3, t4, t5 = st.columns(5)

        with t1:
            st.image(trend_posters[0])
            st.caption(trend_names[0])

        with t2:
            st.image(trend_posters[1])
            st.caption(trend_names[1])

        with t3:
            st.image(trend_posters[2])
            st.caption(trend_names[2])

        with t4:
            st.image(trend_posters[3])
            st.caption(trend_names[3])

        with t5:
            st.image(trend_posters[4])
            st.caption(trend_names[4])

        # MOVIE SELECT
        selected_movie = st.selectbox(
            "Select Movie",
            movies["title"].values
        )

        # GENRE FILTER
        genre_option = st.selectbox(
            "Select Genre",
            [
                "All",
                "Action",
                "Comedy",
                "Drama",
                "Horror",
                "Romance",
                "Sci-Fi",
                "Thriller"
            ]
        )

        # RECOMMEND BUTTON
        if st.button("Recommend"):

            names, posters = hybrid_recommend(
                selected_movie,
                genre_filter=genre_option
            )

            st.session_state.recommended_names = names
            st.session_state.recommended_posters = posters

        # SHOW RECOMMENDATIONS
        if len(
            st.session_state.recommended_names
        ) > 0:

            names = st.session_state.recommended_names

            posters = st.session_state.recommended_posters

            cols = st.columns(5)

            for i in range(len(names)):

                with cols[i]:

                    st.image(
                        posters[i]
                    )

                    st.caption(
                        names[i]
                    )

                    st.info(
                        explain_recommendation(
                            names[i]
                        )
                    )

                    if st.button(
                        f"❤️ Add {names[i]}",
                        key=f"fav{i}"
                    ):

                        add_favorite(
                            username,
                            names[i]
                        )

                        st.success(
                            "Added to favorites"
                        )

        # LOGOUT BUTTON
        if st.button("Logout"):

            st.session_state.logged_in = False

            st.session_state.username = ""

            st.session_state.recommended_names = []

            st.session_state.recommended_posters = []

            st.rerun()

