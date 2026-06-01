from database import User
from database import session


def signup(username, password):

    existing_user = session.query(User).filter_by(
        username=username
    ).first()

    if existing_user:
        return False

    new_user = User(
        username=username,
        password=password
    )

    session.add(new_user)

    session.commit()

    return True


def login(username, password):

    user = session.query(User).filter_by(
        username=username,
        password=password
    ).first()

    if user:
        return True

    return False