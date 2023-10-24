"""Models for Users"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User"""

    __tablename__ = "users"

    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    email=db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)

    events = db.relationship('Event', backref="user")
    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.first_name}"
    
    @classmethod
    def signup(cls, username, email, password, first_name, phone_number):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            phone_number=phone_number,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Event(db.Model):
    """Event"""

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    is_santa_picked = db.Column(db.Boolean, nullable=False)
    is_event_live = db.Column(db.Boolean, nullable=False)

    participants = db.relationship('Participant', backref="participants.event_id")

    
    def serialize(self):
        """Serialize to dictonary"""

        return {
            "id": self.id,
            "owner": self.owner,
            "title": self.title,
            "deadline": self.deadline,
            "is_santa_picked": self.is_santa_picked,
            "is_event_live": self.is_event_live
        }


class Invite(db.Model):
    """Invites"""

    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Text, db.ForeignKey("events.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

class Participant(db.Model):
    """Participants"""

    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    
class Wishlist(db.Model):
    """Wishlists"""

    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    notes = db.Column(db.Text)

    def serialize(self):

        return {
            "id": self.id,
            "participant_id": self.participant_id,
            "notes": self.notes,
        }

class Wishlist_Item(db.Model):
    """Wishlist items"""

    __tablename__ = "wishlist_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlists.id"), nullable=False)
    gift = db.Column(db.Text)
    url = db.Column(db.Text)
    image = db.Column(db.Text)

    wishlist = db.relationship('Wishlist', backref='items')

    def serialize(self):

        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "gift": self.gift,
            "url": self.url,
            "image": self.image,
        }

class Secret_Santa(db.Model):
    """Secret Santas"""

    __tablename__ = "secret_santas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    gifter = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    giftee = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)