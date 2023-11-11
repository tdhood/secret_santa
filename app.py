"""Flask app for Secret Santa"""
import pdb

from flask import Flask, request, redirect, jsonify, render_template, session, g, flash

# from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
import bcrypt
import sys
import os
from datetime import date

from sqlalchemy.exc import IntegrityError

from back.models import (
    db,
    connect_db,
    User,
    Event,
    Participant,
    Wishlist,
    Wishlist_Item,
)
from back.forms import (
    LoginForm,
    UserSignUpForm,
    WishlistForm,
    WishlistItemForm,
    CSRFProtectForm,
)

load_dotenv()
CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////Users/taylorhood/Documents/Projects/SecretSanta/resources/secret_santa"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# toolbar = DebugToolbarExtension(app)

connect_db(app)


################################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None
    


@app.before_request
def add_form_to_g():
    """adds a CSRF form to Flask global"""

    g.csrf_form = CSRFProtectForm()


def do_login(user):
    """Log in user"""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                first_name=form.first_name.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("users/signup.html", form=form)

        do_login(user)

        print(
            jsonify(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "password": user.password,
                }
            )
        )
        return redirect("/")

    else:
        print(f"form errors= {form.errors}")
        return render_template("users/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login and redirect to home page"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!")
            return redirect("/")

        flash("Invalid Credentials.", "danger")

    return render_template("users/login.html", form=form)

@app.route("/logout", methods=["POST"])
def logout():
    """Handle logout of user and redirect to homepage."""

    if g.csrf_form.validate_on_submit():
        do_logout()
        return redirect("/")
    else:
        raise Exception("GO THROUGH THE PROPER CHANNELS.")



###########################################################################
# General User Routes


@app.get("/<int:user_id>/")


##############################################################################
# General Event Routes


@app.get("/<int:user_id>/Events")
def list_user_events(user_id):
    """Page for listings the events of a user"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    events = (
        Event.query.join(Participant, Participant.event_id == Event.id)
        .filter(Participant.user_id == user_id)
        .all()
    )

    serialized = [e.serialize() for e in events]

    print(jsonify(events=serialized))

    return render_template("home.html", events=events)


@app.get("/<int:user_id>/myEvents")
def list_my_events(user_id):
    """Page for listings the events of a user"""

    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")
    events = (Event.query.filter(Event.owner == user_id)).all()

    serialized = [e.serialize() for e in events]

    return jsonify(events=serialized)
    return render_template("users/all_events.html", events=events)


@app.post("/<int:user_id>/myEvents")
def create_new_event(user_id):
    """Create a new event and adds the creator as a participant"""

    title = request.json["title"] or None
    deadline = date.fromisoformat(request.json["deadline"]) or None
    is_santa_picked = False
    is_event_live = True

    new_event = Event(
        owner=user_id,
        title=title,
        deadline=deadline,
        is_santa_picked=is_santa_picked,
        is_event_live=is_event_live,
    )

    db.session.add(new_event)
    db.session.commit()

    serialized = new_event.serialize()

    event_id = serialized["id"]

    owner_participation = Participant(user_id=user_id, event_id=event_id)
    db.session.add(owner_participation)
    db.session.commit()

    serialized_owner = owner_participation.serialize()

    return jsonify(Event=serialized, Participant=serialized_owner)


@app.patch("/<int:user_id>/myEvents/<int:event_id>")
def edit_event(user_id, event_id):
    """edit event but only if owner or admin"""
    # NOTE: need to makes sure this checks if user is event owner

    event = Event.query.get_or_404(event_id)

    event.title = request.json.get("title", event.title)
    if request.json.get("deadline"):
        event.deadline = date.fromisoformat(request.json.get("deadline"))

    db.session.add(event)
    db.session.commit()

    serialized = event.serialize()

    return jsonify(Event=serialized)


# @app.patch("/<int:user_id>/myEvents/<int:event_id>/status")
# def edit_event_status


@app.route("/<int:user_id>/Events/<int:event_id>", methods=['GET', "POST", "DELETE"])
def show_user_one_event(user_id, event_id):
    """shows a user event info

    Event, Wishlist, Wishlist items

    ...maybe confirmed participants?

    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    event = Event.query.get_or_404(event_id)
    # serialized_event = event.serialize()

    wishlist = (
        Wishlist.query.join(Participant, Participant.event_id == event.id)
        .filter(Participant.user_id == user_id)
        .first()
    )
    
    # wishlist_form = WishlistForm()

    # serialized_wishlist = wishlist.serialize()

    wishlist_items_form = WishlistItemForm()

    wishlist_items = Wishlist_Item.query.filter(
        Wishlist_Item.wishlist_id == wishlist.id
    ).all()

    wishlist_items_form = WishlistItemForm()

    # gift = request.json["gift"] or None
    # url = request.json["url"] or None
    # image = request.json["image"] or None

    # new_wishlist_item = Wishlist_Item(
    #     wishlist_id=wishlist.id, gift=gift, url=url, image=image
    # )

    # db.session.add(new_wishlist_item)
    # db.session.commit()

    # serialized_wishlist_item = new_wishlist_item.serialize()


    serialized_wishlist_items = [w.serialize() for w in wishlist_items]

    # print(f"wishlist = {wishlist}")

    # print(
    #     jsonify(
    #         event=serialized_event,
    #         wishlist=serialized_wishlist,
    #         wishlist_items=serialized_wishlist_items,
    #         new_wishlist_item=serialized_wishlist_item
    #     )
    # )
    return render_template(
        "events/one_event.html",
        user_id=user_id,
        event_id=event_id,
        event=event,
        wishlist=wishlist,
        # wishlist_form=wishlist_form,
        wishlist_items=wishlist_items,
        wishlist_items_form=wishlist_items_form,
    )


##########################################################################################
# Wishlist routes


@app.post("/<int:user_id>/Events/<int:event_id>")
def add_wishlist_item(user_id, event_id):
    """Create a wishlist item"""

    event = Event.query.get_or_404(event_id)

    wishlist = (
        Wishlist.query.join(Participant, Participant.event_id == event.id)
        .filter(Participant.user_id == user_id)
        .first()
    )

    wishlist_items_form = WishlistItemForm()

    gift = wishlist_items_form.gift.data or None
    url = wishlist_items_form.url.data or None
    image = wishlist_items_form.image.data or None
    notes = wishlist_items_form.image.data or None

    new_wishlist_item = Wishlist_Item(
        wishlist_id=wishlist.id, gift=gift, url=url, image=image, notes=notes
    )

    db.session.add(new_wishlist_item)
    db.session.commit()

    return render_template(
        "events/one_event.html",
        user_id=user_id,
        event_id=event_id,
        event=event,
        wishlist=wishlist,
        wishlist_items_form=wishlist_items_form
    )


@app.patch("/<int:user_id>/Events/<int:event_id>/<int:wishlist_id>")
def edit_wishlist(user_id, event_id, wishlist_id):
    """Edit wishlists"""

    wishlist = Wishlist.query.get_or_404(wishlist_id)

    wishlist.notes = request.json.get("notes", wishlist.notes)

    db.session.add(wishlist)
    db.session.commit()

    serialized = wishlist.serialize()

    return jsonify(wishlist=serialized)


@app.post(
    "/<int:user_id>/Events/<int:event_id>/<int:wishlist_id>/<int:wishlist_item_id>/edit"
)
def edit_wishlist_item(user_id, event_id, wishlist_id, wishlist_item_id):
    """Edit wishlist items"""

    wishlist_item = Wishlist_Item.query.get_or_404(wishlist_item_id)

    wishlist_item_form = WishlistItemForm(obj=wishlist_item)

    wishlist_item.gift = request.json.get("gift", wishlist_item.gift)
    wishlist_item.url = request.json.get("url", wishlist_item.url)
    wishlist_item.image = request.json.get("image", wishlist_item.image)
    wishlist_item.notes = request.json.get("notes", wishlist_item.notes)

    if wishlist_item_form.validate_on_submit():
        wishlist_item.gift = wishlist_item_form.gift.data
        wishlist_item.url = wishlist_item_form.url.data
        wishlist_item.image = wishlist_item_form.image.data
        wishlist_item.notes = wishlist_item_form.notes.data


        db.session.add(wishlist_item)
        db.session.commit()

    serialized = wishlist_item.serialize()

    return jsonify(wishlist_item=serialized)


@app.post(
    "/<int:user_id>/Events/<int:event_id>/<int:wishlist_id>/<int:wishlist_item_id>/delete"
)
def delete_wishlist_item(user_id, event_id, wishlist_id, wishlist_item_id):
    """delete wishlist items"""
    # NOTE: check that user_id is the same as the wishlist_id

    wishlist_item = Wishlist_Item.query.get_or_404(wishlist_item_id)
    
    form = CSRFProtectForm()
    
    if form.validate_on_submit():
        db.session.delete(wishlist_item)
        db.session.commit()

        return redirect(f"/{user_id}/Events/{event_id}")
        
    else:
        print('erroring')

###########################################################################
# Homepage

@app.get("/")
def homepage():
    """render homepage"""

    if g.user:
        curr_user_id = g.user.id
        events = (
            Event.query.join(Participant, Participant.event_id == Event.id)
            .filter(Participant.user_id == curr_user_id)
            .all()
        )
        return render_template("home.html", events=events)

    else:
        return render_template("home-anon.html")
