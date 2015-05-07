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
        return render_template('homepage.html')


@app.route('/registrationsuccess', methods=['POST'])
def register():
    """taking registraion info and adding to our database"""
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    q = User.query.filter_by(email=email).all()
 
    if q:
        flash("This email already had an account.")
        return render_template('log_in.html')
    else:
        add_user = User(email=email, password=password, age=age,
                        zipcode=zipcode)
        db.session.add(add_user)
        db.session.commit()
        flash("Welcome to the Realm of the Judgemental Eye!")
        return render_template('homepage.html')

# TO COME:  LOG OUT THING!  Flash message: Logged Out.  Probably need a button.

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()