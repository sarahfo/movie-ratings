"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db  #imported db from model which is SQL Alchemy
from server import app
import datetime

def load_users():
    """Load users from u.user into database."""
    for user_info in open('seed_data/u.user'):
        user_info = user_info.rstrip().replace("|", " ").split()
        zipcode = user_info[4]
        age = user_info[1]
        user_id = user_info[0]
        add_user = User(user_id=user_id, email=None, password=None, age=age, 
                        zipcode=zipcode)
        db.session.add(add_user)
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    for movie_info in open('seed_data/u.item'):
        movie_info = movie_info.strip("\n").split("|")
        """each line from u.item is in a list of separate strings"""
        movie_id = movie_info[0]
        title = movie_info[1]
        
        if title.endswith(')'):
            title = title[:-6]
        
        string_date = movie_info[2]
        
        if len(string_date) > 5:
            released_at = datetime.datetime.strptime(string_date, "%d-%b-%Y")
        else: 
            released_at = None
   
        imdb_url = movie_info[4]
        add_movie = Movie(movie_id=movie_id, title=title, 
                        released_at=released_at, imdb_url=imdb_url)
        db.session.add(add_movie)
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
