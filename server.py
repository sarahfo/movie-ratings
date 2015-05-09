"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/log_in')
def show_login():
    return render_template("log_in.html")


@app.route('/loginsuccessful', methods=['POST'])
def login():
    """getting the text from input form and assigning it variable names"""
    email = request.form["email"]
    password = request.form["password"]

    """querying the user table/class to see if the email/password input
    # matches with email/password in user table/class"""

    q = User.query.filter_by(email=email, password=password).all()
    # an alternate way to do this which is much simpler is elim .all and use .one or .first
    # if q:
        # user_id = q.user_id  (q is now an object bc we used one/first)
        # session['user_id'] = user_id
        # flash("You've successfully logged in!")
        # return render_template('homepage.html')
    # else:
    # #   flash("Invalid information.")
    #     return render_template('log_in.html')
    if q == []:
        flash("Invalid information.")
        return render_template('log_in.html')
    else:
        user_id = q[0].user_id
        session['user_id'] = user_id
        flash("You've successfully logged in!")
        return redirect('/')


@app.route('/registration', methods=['POST'])
def register():
    """taking registration info and adding to our database"""
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    q = User.query.filter_by(email=email).all()

    if q:
        flash("This email already had an account.")
        return redirect('/log_in')
    else:
        add_user = User(email=email, password=password, age=age,
                        zipcode=zipcode)
        db.session.add(add_user)
        db.session.commit()
        user_id = add_user.user_id
        print user_id
        session['user_id'] = user_id
        print session

        flash("Welcome to the Realm of the Judgemental Eye!")
        return redirect('/')


@app.route('/loggedout')
def logout():
    """Log user out of account"""
    if 'user_id' not in session:
        return redirect('/log_in')
    else:
        session.pop('user_id', None)
        flash("You've escaped my judgment....for now.")
        return redirect('/')

    print session


@app.route('/users/<user_id>')
def get_user_profile(user_id):
    """Profile page for one specific user."""
    # Query the User Table to get the age, User Id, Zip, Email.
    u = User.query.get(user_id)
    user_id = u.user_id
    email = u.email
    age = u.age
    zipcode = u.zipcode

    user_ratings = Rating.query.filter_by(user_id=user_id).all()
    #user_ratings is a list of rating objects for the selected user_id

    mvidlist = []
    # print user_ratings[0].movie_id
    for rating in user_ratings:    # going through each object in the list user_ratings, pulling movie ids associated
        user_movie_id = Movie.query.get(rating.movie_id)   #movie_id is now a list of all movie ids for the user_id specified
        mvidlist.append(user_movie_id)
        # print mvidlist
        #list of movie ids the user has rated
    
    for movie_id in mvidlist:
        title = movie_id.title
        print type(title)
    
    return render_template('user_profile.html', user_ratings=user_ratings, email=email, age=age, zipcode=zipcode, 
                user_id=user_id, mvidlist=mvidlist)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()