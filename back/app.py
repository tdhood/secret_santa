"""Flask app for Secret Santa"""
import pdb

from flask import Flask, request, redirect, jsonify, render_template, session, g
from dotenv import load_dotenv
import bcrypt
import sys
import os

from sqlalchemy.exc import IntegrityError

from back.models import db, connect_db, User, Event, Participant, Wishlist, Wishlist_Item
from back.forms import LoginForm, UserSignUpForm, UserEditForm, CSRFProtectForm

load_dotenv()
CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////Users/taylorhood/Documents/Projects/SecretSanta/back/secret_santa"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

connect_db(app)
# print(f"db connect {db}")
# breakpoint()


################################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


# @app.before_request
# def add_form_to_g():
#     """adds a CSRF form to Flask global"""

#     g.csrf_form = CSRFProtectForm()


# def do_login(user):
#     """Log in user"""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Log out user"""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    if there already is a user with that username: flash message and re-present form

    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserSignUpForm()

    if form.validate():
        print("I got to form")
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                first_name=form.first_name.data,
            )
            db.session.commit()
        # except Exception as err:
        #     print(f"unexpected {err=}, {type(err)=}")
        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("templates/users/signup.html", form=form)

        do_login(user)

        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "phone_number": user.phone_number,
                "email": user.email,
            }
        ), redirect("/")

        return redirect("/")

    else:
        print(f"form errors= {form.errors}")
        # return render_template('templates/users/signup.html', form=form)


###########################################################################
# General User Routes


@app.get("/<int:user_id>/")


##############################################################################
# General Event Routes


@app.get("/<int:user_id>/myEvents")
def list_user_created_events(user_id):
    """Page for listings the events of a user"""

    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")
    events = (
        Event.query.join(Participant, Participant.event_id == Event.id)
        .filter(Participant.user_id == user_id)
        .all()
    )

    serialized = [e.serialize() for e in events]

    return jsonify(events=serialized)
    return render_template("users/all_events.html", events=events)


@app.get("/<int:user_id>/myEvents/<int:event_id>")
def show_one_event(user_id, event_id):

    event = Event.query.get_or_404(event_id)

    serialized_event = event.serialize()

    wishlist = (
        Wishlist.query.join(Participant, Participant.event_id == event.id)
        .filter(Participant.user_id == user_id)
        .first()
    )

    serialized_wishlist = wishlist.serialize()

    wishlist_items = Wishlist_Item.query.filter(Wishlist_Item.wishlist_id == wishlist.id).all()
    # wishlist_items = wishlist.items
    # print(f'wishlist_items = {wishlist_items}')

    serialized_wishlist_items = [w.serialize() for w in wishlist_items]

    print(f'wishlist = {wishlist}')

    return jsonify(event=serialized_event, wishlist=serialized_wishlist, wishlist_items=serialized_wishlist_items)
    return render_template("users/one_event.html", event=event)


@app.get("/")
def root():
    """render homepage"""
