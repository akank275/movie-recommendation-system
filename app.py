import streamlit as st
import pickle

from recommender import recommend
from trending import get_trending_movies

from auth import signup
from auth import login

from favorites import add_favorite
from favorites import get_favorites


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
    "Signup"
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

    st.write("Login to get personalized movie recommendations.")


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

  # RECOMMEND BUTTON
if st.button("Recommend"):

    names, posters = recommend(
        selected_movie
    )

    st.session_state.recommended_names = names
    st.session_state.recommended_posters = posters


# SHOW RECOMMENDATIONS
if len(st.session_state.recommended_names) > 0:

    names = st.session_state.recommended_names
    posters = st.session_state.recommended_posters

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

        if st.button(
            f"❤️ Add {names[0]}",
            key="fav1"
        ):
            add_favorite(username, names[0])
            st.success("Added to favorites")

    with col2:
        st.image(posters[1])
        st.caption(names[1])

        if st.button(
            f"❤️ Add {names[1]}",
            key="fav2"
        ):
            add_favorite(username, names[1])
            st.success("Added to favorites")

    with col3:
        st.image(posters[2])
        st.caption(names[2])

        if st.button(
            f"❤️ Add {names[2]}",
            key="fav3"
        ):
            add_favorite(username, names[2])
            st.success("Added to favorites")

    with col4:
        st.image(posters[3])
        st.caption(names[3])

        if st.button(
            f"❤️ Add {names[3]}",
            key="fav4"
        ):
            add_favorite(username, names[3])
            st.success("Added to favorites")

    with col5:
        st.image(posters[4])
        st.caption(names[4])

        if st.button(
            f"❤️ Add {names[4]}",
            key="fav5"
        ):
            add_favorite(username, names[4])
            st.success("Added to favorites")

            username = st.session_state.username

        # SIDEBAR FAVORITES
        st.sidebar.subheader("❤️ Your Favorites")

        favorites = get_favorites(username)

        for fav in favorites:
          st.sidebar.write(fav.movie)
          st.sidebar.success(f"Logged in as {username}")

        # LOGOUT
        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()