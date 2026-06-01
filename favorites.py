from database import Favorite
from database import session


def add_favorite(username, movie):

    favorite = Favorite(
        username=username,
        movie=movie
    )

    session.add(favorite)

    session.commit()


def get_favorites(username):

    favorites = session.query(
        Favorite
    ).filter_by(
        username=username
    ).all()

    return favorites