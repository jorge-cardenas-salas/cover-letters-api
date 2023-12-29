import traceback

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from api.database.daos.dao import Dao
from api.database.database import SessionLocal, Base, engine
from api.models.user_model import UserModel

app = FastAPI()


def get_session() -> SessionLocal:
    """
    We use the SessionLocal class to create a dependency. We need to have an independent database session/connection
    (SessionLocal) per request, use the same session through all the request and then close it after the request
    is finished.

    And then a new session will be created for the next request.

    For that, we will create a new dependency with yield. Our dependency will create a new SQLAlchemy SessionLocal
    that will be used in a single request, and then close it once the request is finished.

    Returns:
        SessionLocal: A DB session to be used once
    """
    # fetch session
    session = SessionLocal()
    try:
        # `yield` returns a generator for the session, aka an iterable that can only iterate once
        # In this case it returns a new Session every time is called, but forgets the previous sessions immediately
        yield session
    finally:
        session.close()


@app.put("/add-users")
def add_users(model: UserModel, session: Session = Depends(get_session)):
    """
    Create the new user in the Database

    Args:
        model (UserModel): The user data to be added
        session (Session): The DB session to be used to store the data
    """
    try:
        return Dao.create_user(session=session, user_model=model)
    except Exception as ex:
        print(f"The horror!!! Exception:{str(ex)}; traceback: {traceback.format_exc()}")
