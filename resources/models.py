"""Models for Users"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    hashed_pwd = bcrypt.generate_password_hash(password).decode('utf8')
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    email=db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    events_created = db.Column(db.Array)

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
            phone_number=phone_number
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
    title = db.Column(db.Text, nullable=False)
    participants = db.Column(db.Array)
    is_santa_picked = db.Column(db.Boolean, nullable=False)
    is_event_live = db.Column(db.Boolean, nullable=False)

class Invite(db.Model):
    """Invites"""

    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)

class UserEvent(db.Model):
    """Event <-> User connection"""

    __tablename__ = "user_event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    secret_santa = db.Column(db.Integer)
    wishlist = db.Column(db.Array, nullable=False)
    helpful_notes = db.Column(db.Text)
    user_ready = db.Column(db.Boolean)

    