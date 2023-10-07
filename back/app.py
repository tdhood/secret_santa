"""Flask app for Secret Santa"""

from flask import Flask, request, jsonify, render_template, session, g
#from dotenv import load_dotenv
import bcrypt

from sqlachemy.exc import IntegrityError
from resources.models import (db, connect_db, User)
from resources.forms import (LoginForm, UserSignUpForm, UserEditForm, CSRFProtectForm)

# load_dotenv()
CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite3://secret_santa'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


################################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    '''If we're logged in, add curr user to Flask global'''

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None

@app.before_request
def add_form_to_g():
    '''adds a CSRF form to Flask global'''

    g.csrf_form = CSRFProtectForm()

def do_login(user):
    '''Log in user'''

    session[CURR_USER_KEY] = user.id

def do_logout():
    '''Log out user'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    '''Handle user signup

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    if there already is a user with that username: flash message and re-present form
    
    '''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserSignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                phone_number=form.phone_nmber.data,
                first_name=form.first_name.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("users/signup.html", form=form)
        
        do_login(user)

        return redirect('/')
    
    else:
        return render_template('users/signup.html', form=form)



@app.get('/')
def root():
    """render homepage"""

