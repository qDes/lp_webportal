from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db


class User(db.Document, UserMixin):
    username = db.StringField(max_length=25, required=True, unique=True)
    password = db.StringField(max_length=150, required=True)
    role = db.StringField(max_length=25)
    email = db.StringField(max_length=100)

    def __repr__(self):
        return f"User {self.username}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"
