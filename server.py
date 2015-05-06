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
def log_in():  

    return render_template("log_in.html")

@app.route('/loginsuccessful', methods=["POST"])
def return_home():

    email = request.form.get("email") 
    password = request.form.get("password")
    """getting the text from input form and assigning it variable names"""

    q = User.query.filter_by(email=email, password=password).one()
    """querying the user table/class to see if the email/password input 
    matches with email/password in user table/class""" 
    user_id = q.user_id


    session['user_id'] = user_id
    #returns the id associated with the object/row 

   #later, we might add if statement for error in login/authentication data.
    
    flash('You have successfully logged in')

    return redirect("/homepage")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()